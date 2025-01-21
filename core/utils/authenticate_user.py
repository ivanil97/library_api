from passlib.context import CryptContext
from sqlalchemy import select
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(user_email: str, user_password, db_model, db):
    try:
        statement = select(db_model).where(db_model.email == user_email)
        target_user = db.execute(statement).scalars().first()
    except HTTPException:
        return False

    if not pwd_context.verify(user_password, target_user.password):
        return False

    return target_user
