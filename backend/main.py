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
missing_column = [col for col in required_columns if col not in df.columns]

if missing_column:
    result['success'] = False
    result['message'] = 'Data validation failed'
    result['errors'].append(f"Missing columns: {', '.join(missing_column)}")

#check that the age is within acceptable range
age_range_min = 0
age_range_max = 130

for age in df.iloc[:, 2]:
    if age < age_range_min:
        result['success'] = False
        result['message'] = 'Data validation failed'
        result['errors'].append(f"Age too low: { age }")

    if age > age_range_max:
        result['success'] = False
        result['message'] = 'Data validation failed'
        result['errors'].append(f"Age too high { age }")

app = FastAPI()

@app.get("/")

def index():
    return result

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)