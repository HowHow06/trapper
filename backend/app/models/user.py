from typing import Optional

from app.models import TimestampModel
from pydantic import EmailStr
from sqlmodel import Field


class User(TimestampModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    username: str = Field(index=True, max_length=100)
    hashed_password: str = Field(max_length=100)
    email: EmailStr
    is_admin: bool = Field(default=False)
    is_active: bool = Field(default=True)
