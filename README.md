# Data Quality Service

Server-side data validation with an API that accepts a CSV file and a set of data validation parameters

Simple client-side ReactJS frontend to trigger the data validation

API: FastAPI
Backend: Python, Pandas, Pandera
Frontend: ReactJS, TypeScript

## Installation: Backend
From root directory:
`
cd backend
`
### Set virtual environment:
`
python3 -m venv .venv
`
`
source .venv/bin/activate
`
### Install Dependencies
`
pip install fastapi pandas pandera
`
### Start FastAPI Development Server
`
fastapi dev
`
## Call the API using a browser or postman GET request
http://localhost:8000/validate
## Installation: FrontEnd
From root directory:
`
cd frontend
`
`
npm install
`
### Start the development server
`
npm run dev
`
### Launch the app in the browser
Visit http://localhost:5173/
