from pydantic import BaseModel
from datetime import date, datetime

class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    reg_date: datetime

    class Config:
        from_attributes = True

class BookBase(BaseModel):
    author: str
    description: str
    publish_date: date
    title: str
    photo_path: str

class BookCreate(BookBase):
    user_id: int

class BookUpdate(BookBase):
    pass

class Book(BookBase):
    id: int

class Config:
    from_attributes = True

class Comment(BaseModel):
    id: int
    book_id: int
    user_id: int
    text: str
    created_at: datetime
