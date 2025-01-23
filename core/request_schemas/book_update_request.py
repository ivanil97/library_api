from datetime import date
from typing import List, Optional
from pydantic import BaseModel

from core.request_schemas.author_update_request import AuthorUpdateRequest


class BookUpdateRequest(BaseModel):
    """
    Pydantic-модель, валидирующая запрос на обновление данных книги
    """

    title: Optional[str] = None
    description: Optional[str] = None
    publication_date: Optional[date] = None
    authors: Optional[List[AuthorUpdateRequest]] = None
    genres: Optional[List[str]] = None
    quantity_available: Optional[int] = None
