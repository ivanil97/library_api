from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, status
from jose import jwt, JWTError

from core.database import session
from core.settings import settings

from core.utils.get_user_by_email import get_user_by_email

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login")
SECRET_KEY = settings.secret_key
ALGORITHM = 'HS256'


def get_current_user(token: Annotated[str, Depends(oauth2_schema)]):
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

    user = get_user_by_email(username, session)

    if user is None:
        raise credentials_exception

    return user
