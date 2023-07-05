from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


# Shared properties
class ScanRequestBase(BaseModel):
    original_request_data: Optional[str]


# Properties to receive via API on creation
class ScanRequestCreate(ScanRequestBase):
    original_request_data: str
    task_access_key: str  # need to pass the task access key when creating new scan request


# Properties to receive via API on update
class ScanRequestUpdate(ScanRequestBase):
    original_request_data: Optional[str]
    scan_status_id: Optional[int]
    request_endpoint: Optional[str]
    request_information: Optional[str]
    request_hash: Optional[str]
    start_at: Optional[datetime]
    end_at: Optional[datetime]
    task_id: Optional[int]
    pass


class ScanRequestInDBBase(ScanRequestBase):
    id: int
    original_request_data: str
    scan_status_id: int
    request_endpoint: str
    request_information: str
    request_hash: str
    start_at: Optional[datetime]
    end_at: Optional[datetime]
    task_id: int

    class Config:  # A special class that is used to configure the behavior of the Pydantic model
        orm_mode = True  # A configuration option for Pydantic that enables ORM mode, able to read the data directly from SQLAlchemy models, mainly to validate the response model


# Properties to return to client as RESPONSE
class ScanRequest(ScanRequestInDBBase):
    pass


# Properties properties stored in DB
class ScanRequestInDB(ScanRequestInDBBase):
    pass
