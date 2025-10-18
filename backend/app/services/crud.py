from sqlalchemy.orm import Session
from app.models import user_model
from sqlalchemy import select

import models
from schemas import schemas


def get_or_create_user(db: Session, google_profile: dict) -> user_model.User:
    """
    Finds a user by their Google ID. If they don't exist,
    a new user is created in the database.
    """

    # Extract info from the Google profile
    google_id = google_profile.get("sub")  # 'sub' is the standard field for the user's unique ID
    email = google_profile.get("email")
    full_name = google_profile.get("name")
    profile_pic_url = google_profile.get("picture")

    if not google_id or not email:
        raise ValueError("Missing google_id or email from profile")

    # 1. Try to find the user
    user = db.query(user_model.User).filter(user_model.User.oauth_id == google_id).first()

    # stmt = select(user_model.User).where(user_model.User.oauth_id == google_id)
    # user = db.execute(stmt).scalars().first()

    if user:
        return user

    new_user = user_model.User(
        oauth_provider="google",
        oauth_id=google_id,
        email=email,
        full_name=full_name,
        profile_pic_url=profile_pic_url
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Get the new user's ID from the DB

    return new_user


def create_payout_for_user(
        db: Session, payout: schemas.PayoutCreate, user_id: int
) -> models.Payout:
    db_payout = models.Payout(
        **payout.model_dump(),
        user_id=user_id,
        status=models.PayoutStatus.PENDING
    )
    db.add(db_payout)
    db.commit()
    db.refresh(db_payout)
    return db_payout


def get_payouts_by_user(db: Session, user_id: int) -> list[models.Payout]:
    return db.query(models.Payout).filter(
        models.Payout.user_id == user_id
    ).order_by(models.Payout.id.desc()).all()


def update_payout_status(
        db: Session, payout_id: int, status: models.PayoutStatus
) -> models.Payout | None:
    db_payout = db.query(models.Payout).filter(models.Payout.id == payout_id).first()

    if db_payout:
        db_payout.status = status
        db.add(db_payout)
        db.commit()
        db.refresh(db_payout)

    return db_payout