from typing import Optional

from app.crud.base import CRUDBase
from app.models import ScanRequest
from app.schemas.scan_request import ScanRequestCreate, ScanRequestUpdate
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class CRUDScanRequest(CRUDBase[ScanRequest, ScanRequestCreate, ScanRequestUpdate]):
    async def is_new_request_for_task(self, db: AsyncSession, task_id: int, request_hash: str) -> bool:
        # try:
        condition = and_(ScanRequest.task_id == task_id,
                         ScanRequest.request_hash == request_hash)
        existing_records = await crud_scan_request.get_multi(db=db, where=condition)

        if existing_records and len(existing_records) > 0:
            return False

        return True

        # except Exception:
        #     # RedisService.logger.exception("create_urlclassifications error")
        #     return False


crud_scan_request = CRUDScanRequest(ScanRequest)
