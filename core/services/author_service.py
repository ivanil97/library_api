from sqlalchemy.orm import joinedload
from fastapi import HTTPException

from core.models import Author as AuthorModelDB
from sqlalchemy import select


class AuthorService:
    """
    Класс для работы с таблицей Author в базе данных
    """

    def __init__(self, db):
        self.db = db

    def create_author(self, new_author_data: dict):
        """
        Функция для создания автора в базе данных
        """

        new_author = self.get_or_create_author(new_author_data)

        self.db.add(new_author)
        self.db.commit()
        self.db.refresh(new_author)

        return new_author

    def get_author_by_id(self, author_id: int):
        """
        Функция, возвращающая автора по заданному ID
        """

        statement = select(AuthorModelDB).where(AuthorModelDB.id == author_id).options(joinedload(AuthorModelDB.books))
        author = self.db.execute(statement).scalars().first()

        if author:
            return author
        else:
            raise HTTPException(status_code=404, detail="Author not found")

    def get_all_authors(self):
        """
        Функция, возвращающая всех авторов в библиотеке
        """

        all_authors = self.db.execute(select(AuthorModelDB)).scalars().all()

        if all_authors:
            return all_authors
        else:
            raise HTTPException(status_code=404, detail="No authors found")

    def update_author(self, author_id, updated_author_data: dict):
        """
        Функция для обновления данных об авторе в базе данных
        """

        target_author = self.get_author_by_id(author_id)

        for author_property, new_value in updated_author_data.items():
            setattr(target_author, author_property, new_value)

        self.db.commit()
        self.db.refresh(target_author)

        return target_author

    def delete_author(self, author_id: int):
        """
        Функция для удаления автора из базы данных
        """
        target_author = self.get_author_by_id(author_id)
        if target_author:
            self.db.delete(target_author)

            # удаляем все книги автора
            for i_book in target_author.books:
                self.db.delete(i_book)

            self.db.commit()
            return True
        else:
            return False

    def get_or_create_author(self, new_author_data: dict, existing_authors: dict = None):
        """
        Функция для получения существующего автора из базы данных или создания нового
        """

        if not existing_authors:
            existing_authors = self.get_all_authors()
            existing_authors = {i_author.name: i_author for i_author in existing_authors}

        # проверяем уникальность автора по имени, чтобы не создавать нового
        if new_author_data.get('name') in existing_authors:
            new_author = existing_authors[new_author_data.get('name')]
        else:
            new_author = AuthorModelDB(
                name=new_author_data.get('name'),
                bio=new_author_data.get('bio'),
                birthday=new_author_data.get('birthday'),
            )

        return new_author
