from fastapi import FastAPI
from app.routers import chat_router

app = FastAPI()

app.include_router(chat_router.router)

@app.get('/')
async def root():
    return {"message": "Hello Bigger Applications! from main.py "}