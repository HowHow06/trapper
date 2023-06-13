from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr]
    # username: Optional[str] = None
    # is_active: Optional[bool] = True
    # is_superuser: bool = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

# Additional properties stored in DB


class UserInDB(UserInDBBase):
    hashed_password: str

# Additional properties to return via API


class User(UserInDBBase):
    pass
