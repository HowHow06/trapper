import datetime

from sqlmodel import SQLModel, Field
from passlib.hash import bcrypt
from pydantic import EmailStr


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    hashed_password: str
    email: EmailStr
    created_at: datetime.datetime = datetime.datetime.now()
