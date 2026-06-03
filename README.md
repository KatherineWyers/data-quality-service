# Data Quality Service
Server-side data validation with an API that accepts a CSV file and a set of data validation parameters

API: FastAPI
Backend: Python, Pandas

## Enter the backend directory
From the project directory:
`
cd backend
`

## Virtual Environment
First time Installation:
`
python3 -m venv .venv
source .venv/bin/activate
`

## Install FastAPI
`
pip install fastapi pandas pandera
`


## Start FastAPI Development Server
`
fastapi dev
`

## Call the API from the browser
Visit http://127.0.0.1:8000 to view the API response as a JSON object

## Stop the Server
On Mac: Ctrl+C