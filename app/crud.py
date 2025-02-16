from typing import Type

from sqlalchemy.orm import Session
from datetime import date, datetime
from app.models import User, Book, Comment
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

def add_book_db(db: Session, author: str, description: str, publish_date: datetime.date,
                title: str, photo_path: str, price: int) -> Book:
    new_book = Book(
        author=author,
        description=description,
        publish_date=publish_date,
        title=title,
        photo_path=photo_path,
        price=price
    )
    print(new_book.photo_path)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def get_all_books_db(db: Session) -> list[Type[Book]]:
    return db.query(Book).all()

def get_book_db(db: Session, book_id: int) -> Book:
    return db.query(Book).get(book_id)

def update_book_db(
    db: Session,
    book_id: int,
    author: str,
    description: str,
    publish_date: date,
    title: str,
    photo_path: str,  # Теперь принимает строку
    price: int
) -> Book:
    book = db.query(Book).get(book_id)
    if book:
        book.author = author
        book.description = description
        book.publish_date = publish_date
        book.title = title
        book.photo_path = photo_path  # Сохраняем путь как строку
        book.price = price
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

def update_book_likes(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        return None
    book.likes += 1
    db.commit()
    db.refresh(book)
    return book


def add_comment_db(db: Session, book_id: int, user_id: int, text: str) -> Comment:
    new_comment = Comment(book_id=book_id, user_id=user_id, text=text, created_at=datetime.utcnow())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


def get_comments_by_book_db(db: Session, book_id: int) -> list[Comment]:
    return db.query(Comment).filter(Comment.book_id == book_id).order_by(Comment.created_at.desc()).all()