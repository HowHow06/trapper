from typing import Optional

from app.crud.base import CRUDBase
from app.models import ScanRequest
from app.schemas.scan_request import ScanRequestCreate, ScanRequestUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class CRUDScanRequest(CRUDBase[ScanRequest, ScanRequestCreate, ScanRequestUpdate]):
    pass


crud_scan_request = CRUDScanRequest(ScanRequest)
