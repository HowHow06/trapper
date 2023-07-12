from typing import List, Optional

from app.models import TimestampModel
from sqlmodel import Field, Relationship


class Lookup(TimestampModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    type: str = Field(max_length=100)
    name: str = Field(max_length=100)
    slug: str = Field(max_length=100)
    description: Optional[str] = Field(max_length=1000)
    # vulnerabilities: Optional[List["Vulnerability"]] = Relationship(
    #     back_populates="severity_level")
    # the back populates for `vulnerability_type` is not defined here, not important
    scan_requests: Optional[List["ScanRequest"]] = Relationship(
        back_populates="scan_status")
    tasks: Optional[List["Task"]] = Relationship(back_populates="task_status")
