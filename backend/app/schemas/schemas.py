from pydantic import BaseModel, ConfigDict
from app.models.payout_model import PayoutStatus


class UserPublic(BaseModel):
    id: int
    email: str
    full_name: str | None = None
    picture_url: str | None = None

    model_config = ConfigDict(from_attributes=True)

class PayoutCreate(BaseModel):
    amount: float
    currency: str

class PayoutPublic(BaseModel):
    id: int
    amount: float
    currency: str
    status: PayoutStatus

    model_config = ConfigDict(from_attributes=True)

class WebhookPayload(BaseModel):
    payout_id: int
    new_status: str
