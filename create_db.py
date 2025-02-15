from app.models import User, Book  # Сначала импортируем модели
from database import engine, Base  # Затем подключаем базу

# Создание таблиц
Base.metadata.create_all(bind=engine)

print("Таблицы успешно созданы!")