from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from core.database import session
from core.models import User as UserModelDB
from core.settings import settings
from core.utils.authenticate_user import authenticate_user
from core.utils.create_token import create_token


class TokenGetResponse(BaseModel):
    access_token: str
    token_type: str


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenGetResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password, UserModelDB, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect login or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expires_in_minutes)
    token = create_token(user.email, access_token_expires)

    return {'access_token': token, 'token_type': 'bearer'}
