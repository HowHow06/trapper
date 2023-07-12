from typing import List, Optional

from app.crud.base import CRUDBase
from app.models import ScanRequest, Task
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

    async def get_multi_by_owner(
        self, db: AsyncSession, *, created_by_user_id: int, skip: int = 0, limit: int = 100, sort_by: Optional[str] = None,
        desc_order: bool = False, where=None
    ) -> List[ScanRequest]:
        if where is not None:
            condition = and_(Task.created_by_user_id == created_by_user_id,
                             where)
        else:
            condition = Task.created_by_user_id == created_by_user_id
        return await super().get_multi(db, skip=skip, limit=limit, where=condition, sort_by=sort_by, desc_order=desc_order, join=Task)


crud_scan_request = CRUDScanRequest(ScanRequest)
