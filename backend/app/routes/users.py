from .auth import login_google, google_callback, get_current_user
from fastapi import APIRouter, Depends, Request
from app.schemas import user_schema
from app.models import user_model
from app.db.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/login")
async def login_user(request: Request, code: str = None, state: str = None, db: Session = Depends(get_db)):
    if not code:
        return login_google(request)
    return await google_callback(request, code, state, db)

@router.get("/me", response_model=user_schema.UserPublic)
def get_current_user_profile(current_user: user_model.User = Depends(get_current_user)):
    return current_user
