from datetime import timedelta, datetime

from jose import jwt

from core.settings import settings

SECRET_KEY = settings.secret_key
ALGORITHM = 'HS256'


def create_token(user_email: str, expires_delta: timedelta):
    """
    Создает токен для аутентификации пользователя
    """
    encode = {'username': user_email}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    encoded_jwt = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
