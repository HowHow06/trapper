from typing import List, Optional

from pydantic import BaseModel


# Shared properties
class ResultBase(BaseModel):
    request_id: Optional[int]
    vulnerability_id: Optional[int]
    payload: Optional[str]


# Properties to receive via API on creation
class ResultCreate(ResultBase):
    request_id: int
    vulnerability_id: int
    payload: str


# Properties to receive via API on update
class ResultUpdate(ResultBase):
    pass


class ResultInDBBase(ResultBase):
    id: int
    request_id: int
    vulnerability_id: int
    payload: str

    class Config:  # A special class that is used to configure the behavior of the Pydantic model
        orm_mode = True  # A configuration option for Pydantic that enables ORM mode, able to read the data directly from SQLAlchemy models, mainly to validate the response model


# Properties to return to client as RESPONSE
class Result(ResultInDBBase):
    pass


# Properties properties stored in DB
class ResultInDB(ResultInDBBase):
    pass
