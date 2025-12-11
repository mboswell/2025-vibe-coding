import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from dotenv import load_dotenv

load_dotenv()

from routers import todos

app = FastAPI()

# Include routers
app.include_router(todos.router)


@app.get("/")
async def root():
    """Serve the main index.html page."""
    return FileResponse("frontend/index.html")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
