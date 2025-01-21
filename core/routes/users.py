from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError

from core.request_schemas import UserCreateRequest, UserUpdateRequest
from core.response_schemas import UserGetResponse

from core.models import User as UserModelDB
from sqlalchemy import select

from core.database import session
from core.utils import get_password_hash
from core.utils.get_user_by_email import get_user_by_email
from core.utils.role_checker import RoleChecker

router = APIRouter(prefix="/users", tags=["users"])
role_checker = Depends(RoleChecker(['admin']))
update_role_checker = Depends(RoleChecker(['user']))


@router.get("/", response_model=List[UserGetResponse], status_code=200, dependencies=[role_checker])
async def get_users():
    """
    Эндпоинт для получения списка пользователей
    """
    all_users = session.execute(select(UserModelDB)).scalars().all()
    if not all_users:
        raise HTTPException(status_code=404, detail="No users found")
    return all_users


@router.post("/signup", status_code=201)
async def create_user(new_user: UserCreateRequest):
    """
    Эндпоинт для регистрации нового пользователя
    """

    new_user_db = UserModelDB()
    new_user_db.first_name = new_user.first_name
    new_user_db.last_name = new_user.last_name
    new_user_db.role = new_user.role
    new_user_db.email = new_user.email
    new_user_db.password = get_password_hash(new_user.password)

    try:
        session.add(new_user_db)
        session.commit()
        session.refresh(new_user_db)

        return {"message": "User registered", "user_id": new_user_db.id}
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists")


@router.patch("/{user_id}", status_code=200, dependencies=[update_role_checker])
async def update_user(user_email: str, user: UserUpdateRequest):
    target_user = get_user_by_email(user_email, session)

    new_data = user.model_dump(exclude_unset=True)

    for user_property, new_value in new_data.items():
        setattr(target_user, user_property, new_value)

    session.commit()

    return {"message": "User updated", "user_name": user.email}
