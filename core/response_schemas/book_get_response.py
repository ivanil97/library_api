from datetime import date
from typing import List
from pydantic import BaseModel

from core.response_schemas import AuthorGetResponse


class BookGetResponse(BaseModel):
    """
    Pydantic-модель, описывающая ответ на получение книги
    """

    title: str
    description: str
    publication_date: date
    authors: List[AuthorGetResponse]
    genres: List[str]
    quantity_available: int
