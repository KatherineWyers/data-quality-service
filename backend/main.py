import uvicorn
from fastapi import FastAPI
import json
import pandas as pd


result = {
    'success': True,
    'message': 'Data validation passed successfully',
    'errors': []
}


df = pd.read_csv("test-assets/test-users.csv")
print(df.head())

#check that the required columns are present in the dataframe
required_columns = ["id", "name", "age"]
missing = [col for col in required_columns if col not in df.columns]

if missing:
    result['success'] = False
    result['message'] = 'Data validation failed'
    result['errors'].append(f"Missing columns: {', '.join(missing)}")

app = FastAPI()

@app.get("/")

def index():
    return result

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)