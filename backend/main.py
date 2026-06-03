import io
import pandas as pd
import pandera.pandas as pa
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from rules import RULES

app = FastAPI()

CSV_PATH = "test-assets/test-users.csv"

@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <html>
      <body>
        <h2>CSV Validator</h2>
        <button onclick="runValidation()">Run Validation</button>
        <pre id="result" style="margin-top: 1rem;"></pre>

        <script>
          async function runValidation() {
            document.getElementById("result").textContent = "Running...";
            const res = await fetch("/validate");
            const data = await res.json();
            document.getElementById("result").textContent = JSON.stringify(data, null, 2);
          }
        </script>
      </body>
    </html>
    """

@app.get("/validate")
def validate_csv():
    df = pd.read_csv("test-assets/test-users.csv")

    try:
        RULES.validate(df, lazy=True) #Lazy is Pandera term for loading all errors before returning
        return {"valid": True, "message": "All rows valid.", "error_count": 0, "errors": []}

    except pa.errors.SchemaErrors as e:
        errors = e.failure_cases[["column", "index", "failure_case", "check"]]
        #columns: The column that failed
        #index: The row that failed
        #failure_cases: The value that failed
        #check: The rule that was broken
        errors = errors.rename(columns={"index": "row", "failure_case": "bad_value"})
        return JSONResponse(
            status_code=422,
            content={
                "valid": False,
                "error_count": len(errors),
                "errors": errors.to_dict(orient="records"),
            },
        )