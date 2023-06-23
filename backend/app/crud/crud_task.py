from typing import Optional

from app.crud.base import CRUDBase
from app.models import Task
from app.schemas.task import TaskCreate, TaskUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    pass


crud_task = CRUDTask(Task)
