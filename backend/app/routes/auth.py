# app/routes/auth.py
import base64
import hashlib
import os
import secrets
import urllib.parse
import urllib.parse
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
from app.services import crud
from app.db.database import get_db
import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services import crud

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_AUTH_REDIRECT_URI")
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


def generate_pkce():
    # Generate a code_verifier: between 43 and 128 chars, URL-safe, no padding
    code_verifier = base64.urlsafe_b64encode(os.urandom(64)).decode("utf-8").rstrip("=")

    # Create a SHA256 hash, then base64url encode it, again stripping padding
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode("utf-8")).digest()
    ).decode("utf-8").rstrip("=")

    return code_verifier, code_challenge


@router.get("/google")
def login_google(request: Request):
    state = secrets.token_urlsafe(16)
    nonce = secrets.token_urlsafe(16)

    code_verifier, code_challenge = generate_pkce()

    request.session["state"] = state
    request.session["code_verifier"] = code_verifier

    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "response_type": "code",
        "scope": "openid email profile",
        "redirect_uri": REDIRECT_URI,
        "state": state,
        "nonce": nonce,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "access_type": "offline",
        "prompt": "consent"
    }
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)
    print(url)
    return RedirectResponse(url)

@router.get("/google/callback")
async def google_callback(
    request: Request,
    code: str = None,
    state: str = None,
    db: Session = Depends(get_db)
):
    session_state = request.session.get("state") if hasattr(request, "session") else None
    if state != session_state:
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    code_verifier = request.session.get("code_verifier") if hasattr(request, "session") else None

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code_verifier": code_verifier,
    }

    async with httpx.AsyncClient() as client:
        token_response = await client.post(token_url, data=data)
        token_json = token_response.json()

    if "error" in token_json:
        raise HTTPException(status_code=400, detail=token_json["error"])

    userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
    headers = {"Authorization": f"Bearer {token_json['access_token']}"}
    async with httpx.AsyncClient() as client:
        userinfo_response = await client.get(userinfo_url, headers=headers)
        userinfo = userinfo_response.json()

    try:
        crud.get_or_create_user(db=db, google_profile=userinfo)
        print("Successfully saved user")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    access_token = token_json["access_token"]

    return JSONResponse({"access_token": access_token, "token_type": "Bearer"})


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db),
):
    token = credentials.credentials

    # Verify token with Google
    async with httpx.AsyncClient() as client:
        resp = await client.get(GOOGLE_USERINFO_URL, headers={"Authorization": f"Bearer {token}"})

    if resp.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    userinfo = resp.json()

    user = crud.get_or_create_user(db=db, google_profile=userinfo)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user

