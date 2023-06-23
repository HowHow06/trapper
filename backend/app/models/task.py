from typing import List, Optional

from app.models import TimestampModel
from app.models.lookup import Lookup
from app.models.user import User
from sqlmodel import Field, Relationship


class Task(TimestampModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_status_id: int = Field(default=None, foreign_key="lookup.id")
    task_status: Optional[Lookup] = Relationship(back_populates="tasks")
    created_by_user_id: int = Field(foreign_key="user.id")
    created_by_user: Optional[User] = Relationship(back_populates="tasks")
    task_name: str = Field(max_length=100)
    access_key: str = Field(max_length=255)
    url_rule: str = Field(max_length=100)
    scan_requests: Optional[List["ScanRequest"]
                            ] = Relationship(back_populates="task")
