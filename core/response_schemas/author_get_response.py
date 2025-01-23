from datetime import date
from pydantic import BaseModel


class AuthorGetResponse(BaseModel):
    """
    Pydantic-модель, описывающая ответ на получение автора
    """

    id: int
    name: str
    bio: str
    birthday: date
