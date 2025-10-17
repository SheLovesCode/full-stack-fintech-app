# app/main.py
from fastapi import FastAPI
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware
import os
from app.routes import auth

load_dotenv()
app = FastAPI(title="My FastAPI App")
app.include_router(auth.router)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY"))

@app.get("/")
def root():
    return {"message": "Backend is running!"}
