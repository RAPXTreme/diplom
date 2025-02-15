from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from app.models import *
from database import engine, Base
from sqlalchemy.exc import SQLAlchemyError
from starlette.templating import Jinja2Templates
import os
from app import app
from app.routes import router



app = FastAPI()

try:
        Base.metadata.create_all(bind=engine)
except SQLAlchemyError as e:
        print(f"Ошибка при создании таблиц: {e}")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def home(request):
    return templates.TemplateResponse("home.html", {"request": request})


app.include_router(router)
