# app/main.py
from fastapi import FastAPI
from app.routes.test_router import router as test_router

app = FastAPI(title="My FastAPI App")
app.include_router(test_router)

@app.get("/")
def root():
    return {"message": "Backend is running!"}
