from typing import Optional

from app.crud.base import CRUDBase
from app.models import Lookup
from app.schemas.lookup import LookupCreate, LookupUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class CRUDLookup(CRUDBase[Lookup, LookupCreate, LookupUpdate]):
    pass


crud_lookup = CRUDLookup(Lookup)
