# app/main.py
from fastapi import FastAPI
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware
import os
from app.db.database import Base, engine

load_dotenv()
from app.routes import auth

app = FastAPI(title="Diana's Fullstack Fintech App")
app.include_router(auth.router)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY"))
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Backend is running!"}
