from datetime import date
from typing import Optional

from pydantic import BaseModel


class AuthorUpdateRequest(BaseModel):
    """
    Pydantic-модель, валидирующая запрос на обновление данных автора
    """

    name: Optional[str] = None
    bio: Optional[str] = None
    birthday: Optional[date] = None
