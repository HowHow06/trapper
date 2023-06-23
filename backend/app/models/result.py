from datetime import datetime
from typing import Optional

from app.models import TimestampModel
from app.models.lookup import Lookup
from app.models.scan_request import ScanRequest
from app.models.task import Task
from app.models.vulnerability import Vulnerability
from sqlmodel import Field, Relationship


class Result(TimestampModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    request_id: int = Field(foreign_key="scan_request.id")
    scan_request: ScanRequest = Relationship(
        back_populates="results")
    vulnerability_id: int = Field(foreign_key="vulnerability.id")
    vulnerability: Vulnerability = Relationship(
        back_populates="results")
    payload: str
