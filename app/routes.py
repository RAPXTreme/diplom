import datetime
import logging
from app import schemas
from fastapi import APIRouter, HTTPException, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.schemas import UserCreate, UserLogin, BookCreate, BookUpdate, Book as BookSchema
from app.crud import create_user, authenticate_user, add_book_db, get_all_books_db, get_book_db, update_book_db, delete_book_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")

logger = logging.getLogger(__name__)

from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import get_db
from app.models import Book
import shutil
import os
from typing import List

UPLOAD_DIR = "static/"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Создадим папку, если её нет


@router.post("/books/new")
async def create_book(
        title: str = Form(...),
        author: str = Form(...),
        description: str = Form(...),
        publish_date: str = Form(...),
        file: UploadFile = File(None),
        db: Session = Depends(get_db)
):
    file_path = None

    if file:
        file_path = f"{UPLOAD_DIR}/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    book = Book(
        title=title,
        author=author,
        description=description,
        publish_date=publish_date,
        photo_path=file_path
    )

    db.add(book)
    db.commit()
    db.refresh(book)

    return {"message": "Book added successfully", "book": book}


@router.get("/home", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    try:
        books = get_all_books_db(db)
        return templates.TemplateResponse("home.html", {"request": request, "books": books})
    except Exception as e:
        logger.error(f"Error in home: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register", response_class=HTMLResponse)
async def register_user(request: Request, db: Session = Depends(get_db), email: str = Form(...), username: str = Form(...), password: str = Form(...)):
    try:
        create_user(db, email, username, password)
        return RedirectResponse("/login", status_code=303)
    except Exception as e:
        logger.error(f"Error in register_user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_class=HTMLResponse)
async def login_user(request: Request, db: Session = Depends(get_db), username: str = Form(...), password: str = Form(...)):
    try:
        user = authenticate_user(db, username, password)
        if user:
            return RedirectResponse("/home", status_code=303)
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    except Exception as e:
        logger.error(f"Error in login_user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/books/new", response_class=HTMLResponse)
async def create_book_form(request: Request):
    return templates.TemplateResponse("add_book.html", {"request": request})

@router.post("/books", response_class=HTMLResponse)
async def create_book(request: Request, db: Session = Depends(get_db), author: str = Form(...),
                      description: str = Form(...), publish_date: datetime.date = Form(...), title: str = Form(...),
                      user_id: int = Form(...), photo_path:str = Form(...), price: str = Form(...)):
    try:
        add_book_db(db, author, description, publish_date, title, user_id, photo_path, price)
        return RedirectResponse("/home", status_code=303)
    except Exception as e:
        logger.error(f"Error in create_book: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/books/{book_id}/edit", response_class=HTMLResponse)
async def update_book_form(request: Request, book_id: int, db: Session = Depends(get_db)):
    try:
        book = get_book_db(db, book_id)
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return templates.TemplateResponse("book_form.html", {"request": request, "book": book})
    except Exception as e:
        logger.error(f"Error in update_book_form: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/books/{book_id}", response_class=HTMLResponse)
async def update_book(request: Request, book_id: int, db: Session = Depends(get_db), author: str = Form(...), description: str = Form(...), publish_date: str = Form(...), title: str = Form(...)):
    try:
        update_book_db(db, book_id, author, description, publish_date, title)
        return RedirectResponse("/home", status_code=303)
    except Exception as e:
        logger.error(f"Error in update_book: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/books/{book_id}/delete", response_class=HTMLResponse)
async def delete_book(request: Request, book_id: int, db: Session = Depends(get_db)):
    try:
        delete_book_db(db, book_id)
        return RedirectResponse("/home", status_code=303)
    except Exception as e:
        logger.error(f"Error in delete_book: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    books = get_all_books_db(db)
    return templates.TemplateResponse("home.html", {"request": request, "books": books})
