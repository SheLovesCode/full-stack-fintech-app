# app/routes/auth.py
import base64
import hashlib
import os
import secrets
import urllib.parse
import httpx
from fastapi import Request, HTTPException, Depends, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.services import crud
from app.db.database import get_db

# --- Optional: you can remove router if you're not exposing endpoints here ---
# from fastapi import APIRouter
# router = APIRouter(prefix="/auth", tags=["auth"])

security = HTTPBearer()

# --- Google OAuth constants ---
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_AUTH_REDIRECT_URI")
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


# --- Step 1: PKCE generation ---
def generate_pkce():
    code_verifier = base64.urlsafe_b64encode(os.urandom(64)).decode("utf-8").rstrip("=")
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode("utf-8")).digest()
    ).decode("utf-8").rstrip("=")
    return code_verifier, code_challenge


# --- Step 2: Start login process ---
def login_google(request: Request):
    """
    Starts the Google OAuth flow and returns a redirect response to the Google login URL.
    """
    state = secrets.token_urlsafe(16)
    nonce = secrets.token_urlsafe(16)
    code_verifier, code_challenge = generate_pkce()

    # Store temporary state in session
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
        "prompt": "consent",
    }

    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)
    return RedirectResponse(url)


# --- Step 3: Handle Google callback ---
async def google_callback(
    request: Request,
    code: str,
    state: str,
    db: Session,
):
    """
    Exchanges the authorization code for a token and retrieves the Google user profile.
    """
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

    # Exchange code for tokens
    async with httpx.AsyncClient() as client:
        token_response = await client.post(token_url, data=data)
        token_json = token_response.json()

    if "error" in token_json:
        raise HTTPException(status_code=400, detail=token_json["error"])

    # Fetch user info from Google
    headers = {"Authorization": f"Bearer {token_json['access_token']}"}
    async with httpx.AsyncClient() as client:
        userinfo_response = await client.get(GOOGLE_USERINFO_URL, headers=headers)
        userinfo = userinfo_response.json()

    # Store user in DB
    crud.get_or_create_user(db=db, google_profile=userinfo)

    return JSONResponse({
        "access_token": token_json["access_token"],
        "token_type": "Bearer"
    })


# --- Step 4: Validate a user's token on protected routes ---
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    Validates a Google access token and returns the user record from the DB.
    """
    token = credentials.credentials

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
