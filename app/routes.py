import datetime
import logging
import stripe
from fastapi import APIRouter, HTTPException, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.schemas import UserCreate, UserLogin, BookCreate, BookUpdate, Book as BookSchema, CommentCreate
from app.crud import create_user, authenticate_user, add_book_db, get_all_books_db, get_book_db, update_book_db, delete_book_db, update_book_likes, add_comment_db, get_comments_by_book_db
from database import get_db
from .models import Book, User, Comment
import os
from dotenv import load_dotenv




router = APIRouter()
templates = Jinja2Templates(directory="templates")

logger = logging.getLogger(__name__)

from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import get_db
from app.models import Book
import shutil
import os


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
async def create_book(
        request: Request,
        db: Session = Depends(get_db),
        author: str = Form(...),
        description: str = Form(...),
        publish_date: datetime.date = Form(...),
        title: str = Form(...),
        price: int = Form(...),
        photo: UploadFile = File(...)
):
    try:
        upload_dir = "static/uploads"
        os.makedirs(upload_dir, exist_ok=True)

        timestamp = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{photo.filename}"
        file_path = os.path.join(upload_dir, filename)

        with open(file_path, "wb") as f:
            content = await photo.read()
            f.write(content)

        stored_photo_path = f"/static/uploads/{filename}"

        add_book_db(db, author, description, publish_date, title, stored_photo_path, price)

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
async def update_book(
    request: Request,
    book_id: int,
    db: Session = Depends(get_db),
    author: str = Form(...),
    description: str = Form(...),
    publish_date: str = Form(...),
    title: str = Form(...),
    price: int = Form(...),
    photo: UploadFile = File(None)  # Делаем параметр необязательным
):
    try:
        book = get_book_db(db, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        # Сохраняем текущий путь, если файл не загружен
        file_path = book.photo_path

        # Если загружен новый файл
        if photo and photo.filename:
            upload_dir = "static/uploads"
            os.makedirs(upload_dir, exist_ok=True)
            timestamp = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
            filename = f"{timestamp}_{photo.filename}"
            file_path = os.path.join(upload_dir, filename)
            with open(file_path, "wb") as f:
                content = await photo.read()
                f.write(content)
            file_path = f"/static/uploads/{filename}"

        # Преобразование даты
        publish_date_obj = datetime.datetime.strptime(publish_date, "%Y-%m-%d").date()

        # Обновляем данные
        update_book_db(
            db=db,
            book_id=book_id,
            author=author,
            description=description,
            publish_date=publish_date_obj,
            title=title,
            photo_path=file_path,
            price=price
        )
        return RedirectResponse("/home", status_code=303)
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/books/{book_id}/delete", response_class=HTMLResponse)
async def delete_book(request: Request, book_id: int, db: Session = Depends(get_db)):
    try:
        delete_book_db(db, book_id)
        return RedirectResponse("/home", status_code=303)
    except Exception as e:
        logger.error(f"Error in delete_book: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/books/{book_id}/like")
def like_book(book_id: int, db: Session = Depends(get_db)):
    book = update_book_likes(db, book_id)
    return RedirectResponse(url="/", status_code=303)



STRIPE_SECRET_KEY = "sk_test_51Qt5BEQp32j9YpoeCjyFceIZOFMaw1Nd25l7EpCod9qqbYo8OIMcNv5iQNwZuqJo1xMTjsf1wTPwhG9Bhh5Z7t1800pubYpDW6"
stripe.api_key = STRIPE_SECRET_KEY




@router.post("/payment")
async def process_payment(
        book_id: int = Form(...),
        user_id: int = Form(None),  # Сделаем user_id необязательным
        db: Session = Depends(get_db)
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    amount = book.price * 100  # Stripe принимает сумму в центах
    currency = "USD"
    description = "Покупка без пользователя"

    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user and user.description:
            description = user.description

    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            description=description
        )

        # 🔥 После успешной оплаты делаем редирект
        return RedirectResponse(url=f"https://example.com/success?payment_id={payment_intent.id}", status_code=303)

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=f"Ошибка оплаты: {str(e)}")


@router.post("/books/{book_id}/comments", response_model=None)
async def create_comment(
    book_id: int,
    user_id: int = Form(...),  # Получаем user_id из формы
    text: str = Form(...),      # Получаем text из формы
    db: Session = Depends(get_db)
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    new_comment = Comment(user_id=user_id, book_id=book_id, text=text, created_at=datetime.datetime.utcnow())
    db.add(new_comment)
    db.commit()

    return RedirectResponse(url="/", status_code=303)


@router.get("/books/{book_id}", response_class=HTMLResponse)
def book_detail(request: Request, book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    comments = get_comments_by_book_db(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return templates.TemplateResponse("book_detail.html", {"request": request, "book": book, "comments": comments})
