from sqlalchemy import Table, Column, Integer, String, ForeignKey, Sequence, ARRAY, Date
from sqlalchemy.orm import relationship

from core.database import Base

book_author = Table(
    'book_author', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id', ondelete="CASCADE"), primary_key=True),
    Column('author_id', Integer, ForeignKey('authors.id', ondelete="CASCADE"), primary_key=True)
)


class Book(Base):
    """
    Модель для хранения информации о книге в библиотеке
    """

    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100))
    description = Column(String(1000))
    publication_date = Column(Date)
    genres = Column(ARRAY(String))
    quantity_available = Column(Integer)
    authors = relationship('Author', secondary=book_author, back_populates='books')

    def __str__(self):
        return f'Book {self.id}: {self.title}'
