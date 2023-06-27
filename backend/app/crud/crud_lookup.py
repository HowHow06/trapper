from typing import List, Optional

from app.crud.base import CRUDBase
from app.models import Lookup
from app.schemas.lookup import LookupCreate, LookupUpdate
from slugify import slugify
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class CRUDLookup(CRUDBase[Lookup, LookupCreate, LookupUpdate]):
    async def get_multi_by_type(self, db: AsyncSession, *, type: str) -> List[Lookup]:
        condition = Lookup.type == type
        return await super().get_multi(db, where=condition)

    # encapsulate the password hash function in create
    async def create(self, db: AsyncSession,  *, obj_in: LookupCreate) -> Lookup:
        db_obj = Lookup(
            id=obj_in.id,
            type=obj_in.type,
            name=obj_in.name,
            description=obj_in.description,
            slug=slugify(obj_in.name)
        )
        return await super().create(db, obj_in=db_obj)


crud_lookup = CRUDLookup(Lookup)
