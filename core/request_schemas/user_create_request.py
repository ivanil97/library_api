from pydantic import BaseModel
from typing import Optional


class UserCreateRequest(BaseModel):
    """
    Pydantic-модель, валидирующая запрос на создание пользователя
    """

    first_name: str
    last_name: str
    role: Optional[str]
    email: str
    password: str
