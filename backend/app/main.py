# app/main.py
from fastapi import FastAPI
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware
import os

load_dotenv()
from app.routes import auth
app = FastAPI(title="Diana's Fullstack Fintech App")
app.include_router(auth.router)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY"))

@app.get("/")
def root():
    return {"message": "Backend is running!"}
