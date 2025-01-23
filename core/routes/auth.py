from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from core.response_schemas import TokenGetResponse
from core.services import UserAuthService
from core.settings import settings
from core.utils import get_db_session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenGetResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db_session)):

    auth_service = UserAuthService(db)
    user = auth_service.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect login or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expires_in_minutes)
    token = auth_service.create_token(user.email, access_token_expires)

    return {'access_token': token, 'token_type': 'bearer'}
