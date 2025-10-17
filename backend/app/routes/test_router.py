from fastapi import APIRouter

router = APIRouter(
    prefix="/api",
    tags=["Test"]
)

@router.get("/ping")
def ping():
    return {"message": "pong"}
