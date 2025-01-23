from fastapi import Depends, status
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from core.utils import get_db_session

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from core.services import UserService
from core.settings import settings

from datetime import timedelta, datetime

from jose import jwt, JWTError


oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login")
SECRET_KEY = settings.secret_key
ALGORITHM = 'HS256'


class UserAuthService:
    """
    Сервис для аутентификации пользователя
    """

    def __init__(self, db):
        self.db = db
        self.user_service = UserService(db)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def authenticate_user(self, user_email: str, user_password):
        """
        Функция для аутентификации пользователя
        """

        try:
            target_user = self.user_service.get_user_by_email(user_email)
        except HTTPException:
            return False

        if not self.pwd_context.verify(user_password, target_user.password):
            return False

        return target_user

    @staticmethod
    def get_current_user(token: str = Depends(oauth2_schema),
                         db: Session = Depends(get_db_session)):
        """
        Функция, которая проверяет, существует ли пользователь, передавший токен, в базе, и возвращает его
        """

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("username")

            if username is None:
                raise credentials_exception

        except JWTError:
            raise credentials_exception

        user_service = UserService(db)
        user = user_service.get_user_by_email(username)

        if user is None:
            raise credentials_exception

        return user

    @staticmethod
    def create_token(user_email: str, expires_delta: timedelta):
        """
        Функция для создания токена для аутентификации пользователя
        """

        encode = {'username': user_email}
        expires = datetime.utcnow() + expires_delta
        encode.update({"exp": expires})
        encoded_jwt = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt
