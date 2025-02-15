from typing import Type

from sqlalchemy.orm import Session
from datetime import date
from app.models import User, Book, Comment, Like
from database import get_db

# Функции для работы с пользователями

def create_user(db: Session, email: str, username: str, password: str) -> User:
    new_user = User(email=email, username=username, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_username(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str) -> User:
    user = get_user_by_username(db, username)
    if user and user.password == password:
        return user
    return None

# Функции для работы с книгами

def add_book_db(db: Session, author: str, description: str, publish_date: date, title: str, user_id: int, photo_path: str, price: str) -> Book:
    new_book = Book(author=author, description=description, publish_date=publish_date, title=title, user_id=user_id, photo_path=f'/static/{photo_path}', price=price)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

def get_all_books_db(db: Session) -> list[Type[Book]]:
    return db.query(Book).all()

def get_book_db(db: Session, book_id: int) -> Book:
    return db.query(Book).get(book_id)

def update_book_db(db: Session, book_id: int, author: str, description: str, publish_date: date, title: str) -> Book:
    book = db.query(Book).get(book_id)
    if book:
        book.author = author
        book.description = description
        book.publish_date = publish_date
        book.title = title
        db.commit()
        db.refresh(book)
    return book

def delete_book_db(db: Session, book_id: int) -> bool:
    book = db.query(Book).get(book_id)
    if book:
        db.delete(book)
        db.commit()
        return True
    return False

