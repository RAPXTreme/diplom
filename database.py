from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

SQL_DATABASE_URI = "sqlite:///bookstore.db"
engine = create_engine(SQL_DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
from app.models import *
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()