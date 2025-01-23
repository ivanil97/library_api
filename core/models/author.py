from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from core.database import Base
from core.models.book import book_author


class Author(Base):
    """
    Модель для хранения информации об авторе в библиотеке
    """

    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    bio = Column(String(500))
    birthday = Column(Date)
    books = relationship('Book', secondary=book_author, back_populates='authors')

    def __str__(self):
        return f'Author {self.id}: {self.name}'
