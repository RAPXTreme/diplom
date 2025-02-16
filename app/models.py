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
    price = Column(Integer, default=0.0)
    photo_path = Column(String, nullable=True)
    likes = Column(Integer, default=0)

    user = relationship("User", back_populates="books")
    comments = relationship("Comment", back_populates="book")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"))
    text = Column(String)

    book = relationship("Book", back_populates="comments")

