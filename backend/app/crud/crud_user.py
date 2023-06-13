from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User

from app.crud.base import CRUDBase
from app.core.auth import get_password_hash, verify_password
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_username(self, db: AsyncSession, *, username: str) -> User:
        statement = select(User).filter(User.username == username)
        result = await db.execute(statement)
        # scalars is all objects, return the first object; difference with one() is one must return one object only, if have multiple or zero will throw error
        return result.scalars().first()

    async def get_by_email(self, db: AsyncSession, *, email: str) -> User:
        statement = select(User).filter(User.email == email)
        result = await db.execute(statement)
        return result.scalars().first()

    async def get_by_email_or_username(self, db: AsyncSession, *, email: str,  username: str) -> User:
        user = await self.get_by_username(db, username=username)
        if user:
            return user
        return await self.get_by_email(db, email=email)

    # encapsulate the password hash function in create
    async def create(self, db: AsyncSession,  *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            username=obj_in.username,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: User, obj_in: UserUpdate) -> User:
        update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def authenticate(self, db: AsyncSession, *, username: str, password: str) -> Optional[User]:
        user = await self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


crud_user = CRUDUser(User)
