from datetime import date
from typing import List
from pydantic import BaseModel

from core.request_schemas import AuthorCreateRequest


class BookCreateRequest(BaseModel):
    """
    Pydantic-модель, валидирующая запрос на создание книги
    """

    title: str
    description: str
    publication_date: date
    authors: List[AuthorCreateRequest]
    genres: List[str]
    quantity_available: int
