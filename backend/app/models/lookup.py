from typing import Optional

from app.models import TimestampModel
from sqlmodel import Field


class Lookup(TimestampModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    type: str = Field(max_length=100)
    name: str = Field(max_length=100)
    slug: str = Field(max_length=100)
    description: Optional[str] = Field(max_length=1000)
