from datetime import datetime
from typing import Dict, Generic, List, Optional, Type, TypeVar

from sqlalchemy import and_, delete, desc, select
from sqlalchemy import update as sql_update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        """
         Async implementation of CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A model class that extends SQLModel
        """
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        statement = select(self.model).filter(
            and_(self.model.id == id, self.model.deleted_at.is_(None)))
        result = await db.execute(statement)
        return result.scalars().first()

    # Can add where parameter to this function:
    # from sqlalchemy import or_
    # where_clause = or_(Task.status_id == 1, Task.status_id == 2)
    # result = await crud.get_multi(db, where=where_clause)
    async def get_multi(self, db: AsyncSession, skip: int = 0, limit: int = 100, where=None, sort_by: Optional[str] = None,
                        desc_order: bool = False, join=None) -> List[ModelType]:
        conditions = [self.model.deleted_at.is_(None)]

        if where is not None:
            conditions.append(where)

        statement = select(self.model)
        if join is not None and isinstance(join, list):
            for singleJoin in join:
                statement = statement.join(singleJoin)
                conditions.append(singleJoin.deleted_at.is_(None))
        elif join is not None:
            statement = statement.join(join)
            conditions.append(join.deleted_at.is_(None))

        statement = statement.filter(
            and_(*conditions)).offset(skip).limit(limit)

        if sort_by is not None:
            if hasattr(self.model, sort_by):
                if desc_order:
                    statement = statement.order_by(
                        desc(getattr(self.model, sort_by)))
                else:
                    statement = statement.order_by(
                        getattr(self.model, sort_by))
            else:
                raise ValueError(
                    f"Sort column {sort_by} does not exist on {self.model.__name__}")

        result = await db.execute(statement)
        return result.scalars().all()

    # whatever parameter appear after the * must be explicitly specified when using
    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        if db_obj.deleted_at is not None:
            return db_obj

        obj_data = db_obj.dict()
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    # Sample usage of this function
    # values = {"status_id": 2, "completed_at": datetime.utcnow()}
    # where_clause = Task.status_id == 1
    # updated_rows = await crud.update_by_where(db, values, where=where_clause)
    # print(f"Updated {updated_rows} rows.")
    async def update_by_where(self, db: AsyncSession, values: Dict[str, any], where=None) -> int:
        if not values:
            return 0

        conditions = [self.model.deleted_at.is_(None)]
        if where is not None:
            conditions.append(where)

        stmt = sql_update(self.model).where(and_(*conditions)).values(values)
        result = await db.execute(stmt)
        await db.commit()

        return result.rowcount

    async def remove(self, db: AsyncSession, *, id: int) -> ModelType:
        obj = await self.get(db, id=id)
        # await db.execute(delete(self.model).where(self.model.id == id))
        # await db.commit()
        if obj:
            obj.deleted_at = datetime.utcnow()
            await db.commit()
            await db.refresh(obj)
        return obj
