from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services import crud
from app.schemas import schemas
from app.models import payout_model
from app.db.database import get_db

router = APIRouter(
    prefix="/webhooks",
    tags=["webhooks"]
)


@router.post("/payments")
def handle_payment_webhook(
        payload: schemas.WebhookPayload,
        db: Session = Depends(get_db)
):
    try:
        status_enum = payout_model.PayoutStatus[payload.new_status]
    except KeyError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status value: {payload.new_status}"
        )

    payout = crud.update_payout_status(
        db=db,
        payout_id=payload.payout_id,
        status=status_enum
    )

    if not payout:
        raise HTTPException(
            status_code=404,
            detail=f"Payout with id {payload.payout_id} not found"
        )

    return {"message": "Payout status updated successfully"}
