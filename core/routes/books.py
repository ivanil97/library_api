from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.request_schemas import BookCreateRequest, BookUpdateRequest
from core.response_schemas import BookGetResponse
from core.services import BookService
from core.utils import get_db_session
from core.utils.role_checker import RoleChecker

router = APIRouter(prefix="/books", tags=["books"])
role_checker = Depends(RoleChecker(['admin']))


@router.get("/", response_model=List[BookGetResponse], dependencies=[role_checker])
async def get_books(db: Session = Depends(get_db_session)):
    """
    Эндпойнт для получения списка всех книг
    """

    book_service = BookService(db)
    books = book_service.get_all_books()
    return books


@router.get("/{book_id}", status_code=200, response_model=BookGetResponse)
async def get_book_by_id(book_id: int,
                         db: Session = Depends(get_db_session)):
    """
    Эндпойнт для получения книги по ID
    """

    book_service = BookService(db)
    book = book_service.get_book_by_id(book_id)
    return book


@router.post("/", status_code=201, dependencies=[role_checker])
async def create_book(new_book_data: BookCreateRequest,
                      db: Session = Depends(get_db_session)):
    """
    Эндпойнт для создания новой книги
    """

    book_service = BookService(db)
    new_book = book_service.create_book(new_book_data.model_dump())
    return {"message": "Book added", "book_id": new_book.id}


@router.patch("/{book_id}", status_code=201, dependencies=[role_checker])
async def update_book(updated_book_data: BookUpdateRequest,
                      book_id: int,
                      db: Session = Depends(get_db_session)):
    """
    Эндпойнт для обновления данных книги, найденной по ID
    """

    book_service = BookService(db)
    target_book = book_service.update_book(book_id, updated_book_data.model_dump(exclude_unset=True))
    return {"message": "Book updated", "book_id": target_book.id}


@router.delete("/{book_id}", status_code=200, dependencies=[role_checker])
async def delete_book(book_id: int,
                      db: Session = Depends(get_db_session)):
    """
    Эндпойнт для удаления книги, найденной по ID
    """

    book_service = BookService(db)
    book_service.delete_book(book_id)
    return {"message": "Book deleted", "book_id": book_id}
