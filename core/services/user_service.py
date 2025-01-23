from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from core.models import User as UserModelDB
from core.utils.get_password_hash import get_password_hash


class UserService:
    """
    Класс для работы с таблицей User в базе данных
    """

    def __init__(self, db):
        self.db = db

    def get_all_users(self):
        """
        Функция, возвращающая список всех пользователей
        """

        all_users = self.db.execute(select(UserModelDB)).scalars().all()

        if all_users:
            return all_users
        else:
            raise HTTPException(status_code=404, detail="No users found")

    def create_user(self, new_user_data: dict):
        """
        Функция для создания пользователя в базе данных
        """

        user = UserModelDB()
        user.first_name = new_user_data.get('first_name')
        user.last_name = new_user_data.get('last_name')
        user.role = new_user_data.get('role')
        user.email = new_user_data.get('email')
        user.password = get_password_hash(new_user_data.get('password'))

        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user

        except IntegrityError:
            raise HTTPException(
                status_code=400,
                detail="User with this email already exists")

    def update_user(self, user_email: str, updated_user_data: dict):
        """
        Функция для обновления данных пользователя в базе данных
        """

        target_user = self.get_user_by_email(user_email)

        for user_property, new_value in updated_user_data.items():
            setattr(target_user, user_property, new_value)

        self.db.commit()
        self.db.refresh(target_user)

        return target_user


    def get_user_by_email(self, user_email: str):
        """
        Функция, возвращающая пользователя по заданному email
        """

        statement = select(UserModelDB).where(UserModelDB.email == user_email)
        user = self.db.execute(statement).scalars().first()

        if user:
            return user

        raise HTTPException(
            status_code=404,
            detail='User not found'
        )
