# app/main.py
from fastapi import FastAPI
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware
import os
from app.db import database

load_dotenv()
from app.routes import users

app = FastAPI(title="Diana's Fullstack Fintech App")
app.include_router(users.router)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY"))
database.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def root():
    return {"message": "Backend is running!"}
