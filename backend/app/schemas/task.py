from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


# Shared properties
class TaskBase(BaseModel):
    task_name: Optional[str]
    url_rule: Optional[str]


# Properties to receive via API on creation
class TaskCreate(TaskBase):
    task_name: str
    url_rule: str


# Properties to receive via API on update
class TaskUpdate(TaskBase):
    # task_status_id: Optional[int]
    pass


class TaskInDBBase(TaskBase):
    id: int
    task_status_id: int
    created_by_user_id: int
    task_name: str
    access_key: Optional[str]
    url_rule: str
    app_version: str
    stopped_at: Optional[datetime]

    class Config:  # A special class that is used to configure the behavior of the Pydantic model
        orm_mode = True  # A configuration option for Pydantic that enables ORM mode, able to read the data directly from SQLAlchemy models, mainly to validate the response model


# Properties to return to client as RESPONSE
class Task(TaskInDBBase):
    pass


# Properties properties stored in DB
class TaskInDB(TaskInDBBase):
    pass
