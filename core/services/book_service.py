from sqlalchemy.orm import joinedload
from fastapi import HTTPException

from core.models import Book as BookModelDB
from sqlalchemy import select

from core.services.author_service import AuthorService


class BookService:
    """
    Класс для работы с таблицей Book в базе данных
    """

    def __init__(self, db):
        self.db = db
        self.author_service = AuthorService(db)

    def create_book(self, new_book_data: dict):
        """
        Функция для создания книги в базе данных
        """

        existing_authors = self.author_service.get_all_authors()
        existing_authors = {i_author.name: i_author for i_author in existing_authors}
        new_book_authors = []

        for i_author in new_book_data.get('authors'):
            new_author = self.author_service.get_or_create_author(i_author, existing_authors=existing_authors)
            #     if i_author.get('name') in existing_authors:
            #         new_author = existing_authors[i_author.get('name')]
            #     else:
            #         new_author = AuthorModelDB(
            #             name=i_author.get('name'),
            #             bio=i_author.get('bio'),
            #             birthday=i_author.get('birthday'),
            #         )
            self.db.add(new_author)
            new_book_authors.append(new_author)

        self.db.commit()

        book = BookModelDB(
            title=new_book_data.get('title'),
            description=new_book_data.get('description'),
            publication_date=new_book_data.get('publication_date'),
            authors=new_book_authors,
            genres=new_book_data.get('genres'),
            quantity_available=new_book_data.get('quantity_available')
        )

        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)

        return book

    def get_book_by_id(self, book_id: int):
        """
        Функция, возвращающая книгу по заданному ID
        """

        statement = select(BookModelDB).where(BookModelDB.id == book_id).options(joinedload(BookModelDB.authors))
        book = self.db.execute(statement).scalars().first()

        if book:
            return book
        else:
            raise HTTPException(status_code=404, detail="Book not found")

    def get_all_books(self):
        """
        Функция, возвращающая все книги в библиотеке
        """

        all_books = self.db.execute(select(BookModelDB)).scalars().all()

        if all_books:
            return all_books
        else:
            raise HTTPException(status_code=404, detail="No books found")

    def update_book(self, book_id, updated_book_data: dict):
        """
        Функция для обновления данных книги в базе данных
        """

        target_book = self.get_book_by_id(book_id)

        existing_authors = self.author_service.get_all_authors()
        existing_authors = {i_author.name: i_author for i_author in existing_authors}

        for book_property, new_value in updated_book_data.items():
            if book_property == 'authors':
                target_book.authors = []
                for i_author in new_value:
                    new_author = self.author_service.get_or_create_author(i_author, existing_authors=existing_authors)
                    target_book.authors.append(new_author)
            else:
                setattr(target_book, book_property, new_value)

        self.db.commit()
        self.db.refresh(target_book)

        return target_book

    def delete_book(self, book_id: int):
        """
        Функция для удаления книги из базы данных
        """
        target_book = self.get_book_by_id(book_id)
        if target_book:
            self.db.delete(target_book)
            self.db.commit()
            return True
        else:
            return False
