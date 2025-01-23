from typing import List
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from core.models import User
from core.services import UserAuthService

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login")

class RoleChecker:

    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(UserAuthService.get_current_user)):
        if current_user.role in self.allowed_roles:
            return True

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You do not have a permission to perform this action'
        )
