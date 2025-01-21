from sqlalchemy import select
from fastapi import HTTPException
from core.models import User as UserModelDB


def get_user_by_email(user_email: str, db):
    statement = select(UserModelDB).where(UserModelDB.email == user_email)
    user = db.execute(statement).scalars().first()

    if user:
        return user

    raise HTTPException(
        status_code=404,
        detail='Пользователь с таким email не найден'
    )
