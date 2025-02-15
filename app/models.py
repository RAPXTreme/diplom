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

    books = relationship("Book", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")


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
    likes = relationship("Like", back_populates="book", cascade="all, delete-orphan")

    user = relationship("User", back_populates="books")
    comments = relationship("Comment", back_populates="book")


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))

    user = relationship("User", back_populates="comments")
    book = relationship("Book", back_populates="comments")


class Like(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))

    user = relationship("User", back_populates="likes")
    book = relationship("Book", back_populates="likes")

