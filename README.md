# 2025 Vibe Coding Demo

A to-do list web application built with FastAPI and Databricks Lakebase.

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
- `POST /todos` - Create a new to-do item
- `GET /todos` - List to-do items (use `?include_all=true` to see deleted)
- `PUT /todos/{id}` - Update a to-do item
- `PUT /todos/{id}/status` - Change to-do status
- `DELETE /todos/{id}` - Soft delete a to-do item

## Architecture

- `/routers` - API route handlers
- `/services` - Business logic and database operations
- `/frontend` - Static HTML frontend
