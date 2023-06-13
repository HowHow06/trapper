import datetime

from sqlmodel import SQLModel, Field
from passlib.hash import bcrypt
from pydantic import EmailStr

from app.models import TimestampModel


class User(TimestampModel, table=True):  # table=True will use the class name as table name
    id: int = Field(default=None, primary_key=True, index=True)
    username: str = Field(index=True)
    hashed_password: str
    email: EmailStr
