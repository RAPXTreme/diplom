from app.models import *  # Импортируем модели перед Base
from database import engine
from database import Base  # Затем подключаем базу
from app import app
from sqlalchemy.exc import SQLAlchemyError

def create_tables():
    try:
        print("Создание таблиц...")
        Base.metadata.create_all(bind=engine)
        print("Таблицы успешно созданы!")
    except SQLAlchemyError as e:
        print(f"Ошибка при создании таблиц: {e}")

if __name__ == "__main__":
    create_tables()

    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Starting server...")

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
