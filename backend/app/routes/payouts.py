from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
import time
import random
import httpx

from app.db.database import get_db
from app.routes.auth import get_current_user
from app.models import user_model, payout_model
from app.schemas import schemas
from app.services import crud

router = APIRouter(
    prefix="/payouts",
    tags=["payouts"]
)


def simulate_webhook_call(payout_id: int):
    time.sleep(random.randint(3, 5))

    new_status = random.choice(["PAID", "FAILED"])

    try:
        with httpx.Client() as client:
            client.post(
                "http://localhost:8000/webhooks/payments",
                json={"payout_id": payout_id, "new_status": new_status}
            )
    except Exception as e:
        print(f"Failed to simulate webhook for payout {payout_id}: {e}")


@router.post("/", response_model=schemas.PayoutPublic)
def create_payout(
        payout: schemas.PayoutCreate,
        background_tasks: BackgroundTasks,
        current_user: user_model.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    new_payout = crud.create_payout_for_user(
        db=db, payout=payout, user_id=current_user.id
    )

    background_tasks.add_task(simulate_webhook_call, new_payout.id)

    return new_payout


@router.get("/", response_model=list[schemas.PayoutPublic])
def get_payouts(
        current_user: user_model.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    payouts = crud.get_payouts_by_user(db=db, user_id=current_user.id)
    return payouts