from typing import Optional
from pydantic import BaseModel


class UserUpdateRequest(BaseModel):
    """
    Pydantic-модель, валидирующая запрос на обновление данных пользователя
    """

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None  # TODO: проверить, что при передаче пустого аргумента поле не остается пустым
    email: Optional[str] = None
    password: Optional[str] = None
