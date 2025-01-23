from datetime import datetime, timedelta

from core.services import BookService
from core.models import User as UserModelDB
from fastapi import HTTPException, status


class OperationService:
    """
    Класс для хранения логики выдачи и получения книг
    """

    def __init__(self, db):
        self.db = db
        self.book_service = BookService(db)

    def lend_book(self, user: UserModelDB, book_id: int, book_limit: int = 5, checkout_time: int = 30):
        """
        Функция, реализующая выдачу книг читателю
        """

        if user.books_on_hands >= book_limit:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Limit of books on hands is reached")

        target_book = self.book_service.get_book_by_id(book_id)
        if target_book.quantity_available < 1:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="No books available")

        user.books_on_hands += 1
        target_book.quantity_available -= 1

        lent_date = datetime.utcnow()
        return_date = datetime.utcnow() + timedelta(days=checkout_time)

        self.db.commit()

        return {"message": f"Book {book_id} lent to user {user.id}",
                "lent_date": lent_date,
                "return_date": return_date}


    def return_book(self, user: UserModelDB, book_id: int):
        """
        Функция, реализующая возврат книг читателем
        """

        if user.books_on_hands < 1:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="No books to be returned")

        target_book = self.book_service.get_book_by_id(book_id)

        user.books_on_hands -= 1
        target_book.quantity_available += 1

        factual_return_date = datetime.utcnow()

        self.db.commit()

        return {"message": f"Book {book_id} returned from user {user.id} to library",
                "factual_return_date": factual_return_date}