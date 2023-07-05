from datetime import datetime
from typing import List, Optional

from app.models import TimestampModel
from app.models.lookup import Lookup
from app.models.task import Task
from sqlmodel import Field, Relationship


class ScanRequest(TimestampModel, table=True):
    __tablename__ = "scan_request"
    id: Optional[int] = Field(default=None, primary_key=True)
    original_request_data: str
    payload: Optional[str]
    scan_status_id: int = Field(foreign_key="lookup.id")
    scan_status: Lookup = Relationship(
        back_populates="scan_requests")
    request_endpoint: str = Field(max_length=255)
    request_information: str
    request_hash: str = Field(max_length=255)
    start_at: Optional[datetime]
    end_at: Optional[datetime]
    task_id: int = Field(foreign_key="task.id")
    task: Task = Relationship(back_populates="scan_requests")
    app_version: str = Field(max_length=20)
    result: Optional["Result"] = Relationship(
        # sa_relationship_kwargs={'uselist': False},
        back_populates="scan_request")  # one to one
