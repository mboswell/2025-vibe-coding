import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from dotenv import load_dotenv

load_dotenv()

from services.lakebase import Lakebase

app = FastAPI()


@app.get("/")
async def root():
    """Serve the main index.html page."""
    return FileResponse("frontend/index.html")


@app.get("/api/time")
async def get_database_time():
    """Get the current time from the Lakebase database."""
    try:
        rows = Lakebase.query("SELECT NOW()")
        if rows and len(rows) > 0:
            return {"time": str(rows[0][0]), "status": "success"}
        return {"time": None, "status": "no_result"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
