from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base  # Импортируем Base из database.py


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    reg_date = Column(DateTime, default=datetime.utcnow)  # utcnow лучше для кросс-часовых поясов

    books = relationship("Book", back_populates="user", cascade="all, delete-orphan")  # Каскадное удаление


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False)
    publish_date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    photo_path = Column(String, nullable=True)  # Новое поле для хранения пути к изображению

    user = relationship("User", back_populates="books")
