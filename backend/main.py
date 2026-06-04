import pandas as pd
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from services.validator import ValidatorService

app = FastAPI()

DATA = pd.DataFrame({
    "id": [1, 2, 3, 4],
    "name": ["Jane", "Tom", "Bob","Jim"],
    "age": [25, 30, 34, 67],
})

RULES_JSON = {
    "settings": {
        "strict_columns": True
    },
    "columns": {
        "id": {
            "required": True,
            "type": "one_dim_integer1",
            "validation_params": {"min": 1},
        },
        "name": {
            "required": True,
            "type": "alphatext",
            "validation_params": {"min-length": 3, "max-length": 30},
        },
        "age": {
            "required": True,
            "type": "one_dim_integer",
            "validation_params": {"min": 0, "max": 150},
        },
    }
}

@app.get("/validate")
def validate():
    validator_service = ValidatorService()
    result = validator_service.run(DATA, RULES_JSON)
    return JSONResponse(content=result.to_dict())