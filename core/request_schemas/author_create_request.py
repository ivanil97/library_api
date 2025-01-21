from datetime import date
from pydantic import BaseModel


class AuthorCreateRequest(BaseModel):
    """
    Pydantic-модель, валидирующая запрос на создание автора
    """

    name: str
    bio: str
    birthday: date
