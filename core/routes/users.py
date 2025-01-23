from typing import List

from fastapi import APIRouter, HTTPException, Depends

from core.request_schemas import UserCreateRequest, UserUpdateRequest
from core.response_schemas import UserGetResponse

from sqlalchemy.orm import Session

from core.services import UserService, UserAuthService
from core.utils import get_db_session
from core.utils.role_checker import RoleChecker

from core.models import User as UserModelDB

router = APIRouter(prefix="/users", tags=["users"])
role_checker = Depends(RoleChecker(['admin']))


@router.get("/", response_model=List[UserGetResponse], status_code=200, dependencies=[role_checker])
async def get_users(db: Session = Depends(get_db_session)):
    """
    Эндпоинт для получения списка пользователей
    """

    user_service = UserService(db)
    users = user_service.get_all_users()
    return users


@router.post("/signup", status_code=201)
async def create_user(new_user_data: UserCreateRequest,
                      db: Session = Depends(get_db_session)):
    """
    Эндпоинт для регистрации нового пользователя
    """

    user_service = UserService(db)
    new_user = user_service.create_user(new_user_data.model_dump())
    return {"message": "User registered", "user_id": new_user.id}


@router.patch("/{user_id}", status_code=200)
async def update_user(user_email: str,
                      updated_user_data: UserUpdateRequest,
                      db: Session = Depends(get_db_session),
                      current_user: UserModelDB = Depends(UserAuthService.get_current_user)):
    """
    Функция для обновления данных пользователя в базе данных
    """

    if current_user.email != user_email:
        raise HTTPException(
            status_code=401,
            detail="You can't update other users")

    user_service = UserService(db)
    target_user = user_service.update_user(user_email, updated_user_data.model_dump(exclude_unset=True))
    return {"message": "User updated", "user_name": target_user.email}
