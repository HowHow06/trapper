from typing import Optional

from app.crud.base import CRUDBase
from app.models import Result
from app.schemas.result import ResultCreate, ResultUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class CRUDResult(CRUDBase[Result, ResultCreate, ResultUpdate]):
    pass


crud_result = CRUDResult(Result)
