from datetime import date
from typing import List, Optional
from pydantic import BaseModel

from core.request_schemas import AuthorCreateRequest


class BookUpdateRequest(BaseModel):
    """
    Pydantic-модель, валидирующая запрос на обновление данных книги
    """

    title: Optional[str] = None
    description: Optional[str] = None
    publication_date: Optional[date] = None
    authors: Optional[List[AuthorCreateRequest]] = None
    genres: Optional[List[str]] = None
    quantity_available: Optional[int] = None
