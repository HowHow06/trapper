from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr]
    is_active: Optional[bool] = True
    is_admin: bool = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:  # A special class that is used to configure the behavior of the Pydantic model
        orm_mode = True  # A configuration option for Pydantic that enables ORM mode, able to read the data directly from SQLAlchemy models, mainly to validate the response model


# Properties to return to client as response
class User(UserInDBBase):
    pass

# # Properties properties stored in DB
# class UserInDB(UserInDBBase):
#     hashed_password: str
