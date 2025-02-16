from starlette.staticfiles import StaticFiles
import os
from app import app
from app.models import *
from database import engine
from database import Base
from sqlalchemy.exc import SQLAlchemyError
from starlette.templating import Jinja2Templates



def create_tables():
    try:
        print("Создание таблиц...")
        Base.metadata.create_all(bind=engine)
        print("Таблицы успешно созданы!")
    except SQLAlchemyError as e:
        print(f"Ошибка при создании таблиц: {e}")
static_dir = os.path.join(os.path.dirname(__file__), "static")

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory="templates")

if __name__ == "__main__":
    create_tables()

    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Starting server...")

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")


def home(request):
    return templates.TemplateResponse("home.html", {"request": request})

from app.routes import router
app.include_router(router)