from datetime import datetime
from typing import Optional

from app.models import TimestampModel
from app.models.lookup import Lookup
from app.models.task import Task
from sqlmodel import Field, Relationship


class ScanRequest(TimestampModel, table=True):
    __tablename__ = "scan_request"
    id: Optional[int] = Field(default=None, primary_key=True)
    original_request_data: str
    payload: str
    scan_status_id: int = Field(foreign_key="lookup.id")
    scan_status: Optional[Lookup] = Relationship(
        back_populates="scan_requests")
    request_endpoint: str = Field(max_length=255)
    request_information: str
    request_hash: str = Field(max_length=255)
    start_at: datetime
    end_at: datetime
    task_id: int = Field(foreign_key="task.id")
    task: Optional[Task] = Relationship(back_populates="scan_requests")
    app_version: str = Field(max_length=20)


Task.scan_requests = Relationship(back_populates="task")
Lookup.scan_requests = Relationship(back_populates="scan_status")
