from typing import Optional

from app.core.auth import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models import User
from app.schemas.user import UserCreate, UserUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_username(self, db: AsyncSession, *, username: str) -> User:
        condition = User.username == username
        users = await super().get_multi(db, where=condition)
        # scalars is all objects, return the first object; difference with one() is one must return one object only, if have multiple or zero will throw error
        return users[0] if users else None

    async def get_by_email(self, db: AsyncSession, *, email: str) -> User:
        condition = User.email == email
        users = await super().get_multi(db, where=condition)
        return users[0] if users else None

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
            is_admin=obj_in.is_admin,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        # did not use create function from super class because User schema is used instead of UserCreate schema, to hide the hashed_password field
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: User, obj_in: UserUpdate) -> User:
        if db_obj.deleted_at is not None:
            return db_obj

        update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password

        obj_data = db_obj.dict()
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    async def authenticate(self, db: AsyncSession, *, username: str, password: str) -> Optional[User]:
        user = await self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_admin(self, user: User) -> bool:
        return user.is_admin


crud_user = CRUDUser(User)
