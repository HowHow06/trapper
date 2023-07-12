from typing import List, Optional

from pydantic import BaseModel


# Shared properties
class LookupBase(BaseModel):
    type: Optional[str]
    name: Optional[str]
    description: Optional[str]

# Properties to receive via API on creation


class LookupCreate(LookupBase):
    id: Optional[int]
    type: str
    name: str


# Properties to receive via API on update
class LookupUpdate(LookupBase):
    pass


class LookupInDBBase(LookupBase):
    id: int
    type: str
    name: str
    slug: str

    class Config:  # A special class that is used to configure the behavior of the Pydantic model
        orm_mode = True  # A configuration option for Pydantic that enables ORM mode, able to read the data directly from SQLAlchemy models, mainly to validate the response model


# Properties to return to client as RESPONSE
class Lookup(LookupInDBBase):
    pass


# Properties properties stored in DB
class LookupInDB(LookupInDBBase):
    pass
