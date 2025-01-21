from sqlalchemy import Column, Integer, String, Sequence
from core.database import Base


class User(Base):
    """
    Модель для хранения информации о пользователе
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    role = Column(String, nullable=False, default='user')
    email = Column(String(50), unique=True, index=True)
    password = Column(String(1000))

    def __str__(self):
        return f'User {self.id}: {self.first_name} {self.last_name}'
