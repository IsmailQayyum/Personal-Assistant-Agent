from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from app.routers import chat_router


app = FastAPI()

# Get the absolute path to the project root directory
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
static_dir = os.path.join(BASE_DIR, "static")

# print(f"Base directory: {BASE_DIR}")
# print(f"Static directory: {static_dir}")
# print(f"Static directory exists: {os.path.exists(static_dir)}")

# Create static directory if it doesn't exist
os.makedirs(static_dir, exist_ok=True)

# Mount static files with absolute path
app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(chat_router.router)

@app.get('/')
async def root():
    return {"message": "Hello Bigger Applications! from main.py"}