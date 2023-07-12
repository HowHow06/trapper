from typing import List, Optional

from app.crud.base import CRUDBase
from app.models import Result, ScanRequest, Task
from app.schemas.result import ResultCreate, ResultUpdate
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class CRUDResult(CRUDBase[Result, ResultCreate, ResultUpdate]):
    async def get_multi_by_owner(
        self, db: AsyncSession, *, created_by_user_id: int, skip: int = 0, limit: int = 100, sort_by: Optional[str] = None,
        desc_order: bool = False, where=None
    ) -> List[Result]:
        if where is not None:
            condition = and_(Task.created_by_user_id == created_by_user_id,
                             where)
        else:
            condition = Task.created_by_user_id == created_by_user_id
        return await super().get_multi(db, skip=skip, limit=limit, where=condition, sort_by=sort_by, desc_order=desc_order, join=[ScanRequest, Task])


crud_result = CRUDResult(Result)
