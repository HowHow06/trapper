from typing import List, Optional

from app.core import constants, utils
from app.crud.base import CRUDBase
from app.models import Task
from app.schemas.task import TaskCreate, TaskUpdate
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
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
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        db_obj.access_key = utils.generate_task_access_key(
            user_id=created_by_user_id, task_id=db_obj.id)
        await db.commit()

        return db_obj

    async def get_multi_by_owner(
        self, db: AsyncSession, *, created_by_user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        condition = Task.created_by_user_id == created_by_user_id
        return await super().get_multi(db, skip=skip, limit=limit, where=condition)


crud_task = CRUDTask(Task)
