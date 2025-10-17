# app/routes/auth.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.get("/login/google")
def login_google():
    return {"message": "Google login will go here"}
