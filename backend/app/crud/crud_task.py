from typing import List, Optional

from app.core import constants, task_util
from app.core.config import get_version
from app.crud.base import CRUDBase, CRUDBaseSync
from app.models import Task
from app.schemas.task import TaskCreate, TaskUpdate
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    async def create_with_owner(
        self, db: AsyncSession, *, obj_in: TaskCreate, created_by_user_id: int
    ) -> Task:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(
            **obj_in_data,
            created_by_user_id=created_by_user_id,
            task_status_id=constants.Status.WAITING,
            app_version=get_version()
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        db_obj.access_key = task_util.generate_task_access_key(
            user_id=created_by_user_id, task_id=db_obj.id)
        await db.commit()

        return db_obj

    async def get_multi_by_owner(
        self, db: AsyncSession, *, created_by_user_id: int, skip: int = 0, limit: int = 100, sort_by: Optional[str] = None,
        desc_order: bool = False, where=None
    ) -> List[Task]:
        if where is not None:
            condition = and_(Task.created_by_user_id == created_by_user_id,
                             where)
        else:
            condition = Task.created_by_user_id == created_by_user_id
        return await super().get_multi(db, skip=skip, limit=limit, where=condition, sort_by=sort_by, desc_order=desc_order)


crud_task = CRUDTask(Task)


class CRUDTaskSync(CRUDBaseSync[Task, TaskCreate, TaskUpdate]):
    pass


crud_task_sync = CRUDTaskSync(Task)
