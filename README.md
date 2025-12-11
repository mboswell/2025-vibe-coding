# 2025 Vibe Coding Demo

A simple web application built with FastAPI that connects to a Databricks Lakebase database.

## Technologies

- **FastAPI** - Modern, fast Python web framework
- **Uvicorn** - ASGI server for running the app
- **python-dotenv** - Environment variable management
- **psycopg2** - PostgreSQL adapter for Lakebase connection
- **databricks-sdk** - Databricks SDK for authentication and token generation

## Getting Started

1. Create a `.env` file based on `example.env` with your real values
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python app.py`
4. Visit http://localhost:8000

## API Endpoints

- `GET /` - Serves the main index.html page
- `GET /api/time` - Returns the current time from the Lakebase database
