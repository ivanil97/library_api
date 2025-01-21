from typing import List
from core.models import User as UserModelDB
from fastapi import Depends, HTTPException, status

from core.utils.get_current_user import get_current_user


class RoleChecker:

    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: UserModelDB = Depends(get_current_user)):
        if current_user.role in self.allowed_roles:
            return True

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You do not have a permission to perform this action'
        )
