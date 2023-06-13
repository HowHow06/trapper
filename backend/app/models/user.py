from app.models import TimestampModel
from pydantic import EmailStr
from sqlmodel import Field


class User(TimestampModel, table=True):  # table=True will use the class name as table name
    id: int = Field(default=None, primary_key=True, index=True)
    username: str = Field(index=True)
    hashed_password: str
    email: EmailStr
    is_admin: bool = Field(default=False)
    is_active: bool = Field(default=True)
