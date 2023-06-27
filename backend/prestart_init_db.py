import asyncio
import logging

from app import crud, schemas
from app.core.config import settings
from app.db.session import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init_admin(db: AsyncSession) -> None:
    user = await crud.crud_user.get_by_email_or_username(
        db, email=settings.FIRST_SUPERUSER_EMAIL, username=settings.FIRST_SUPERUSER_USERNAME)
    if not user:
        user_in = schemas.UserCreate(
            username=settings.FIRST_SUPERUSER_USERNAME,
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_admin=True
        )
        user = await crud.crud_user.create(db, obj_in=user_in)


async def init_user(db: AsyncSession) -> None:
    user = await crud.crud_user.get_by_email_or_username(
        db, email=settings.FIRST_USER_EMAIL, username=settings.FIRST_USER_USERNAME)
    if not user:
        user_in = schemas.UserCreate(
            username=settings.FIRST_USER_USERNAME,
            email=settings.FIRST_USER_EMAIL,
            password=settings.FIRST_USER_PASSWORD,
            is_admin=False
        )
        user = await crud.crud_user.create(db, obj_in=user_in)


async def init_lookup_status(db: AsyncSession) -> None:
    statuses = await crud.crud_lookup.get_multi_by_type(
        db, type=settings.LOOKUP_TYPE_STATUS)
    if len(statuses) != 4:
        waiting_status = schemas.LookupCreate(
            id=1,
            type=settings.LOOKUP_TYPE_STATUS,
            name="WAITING",
            description="Status when the task/scan request is created but not processed (for both Scan Request and Task)."
        )
        await crud.crud_lookup.create(db, obj_in=waiting_status)
        running_status = schemas.LookupCreate(
            id=2,
            type=settings.LOOKUP_TYPE_STATUS,
            name="RUNNING",
            description="Status when the task/scan request is being processed (for both Scan Request and Task)."
        )
        await crud.crud_lookup.create(db, obj_in=running_status)
        done_status = schemas.LookupCreate(
            id=3,
            type=settings.LOOKUP_TYPE_STATUS,
            name="DONE",
            description="Status when the task/scan request is completed (for both Scan Request and Task)."
        )
        await crud.crud_lookup.create(db, obj_in=done_status)
        killed_status = schemas.LookupCreate(
            id=4,
            type=settings.LOOKUP_TYPE_STATUS,
            name="KILLED",
            description="Status when the task is killed when user click the stop task button, right before the task is done (for Task only)."
        )
        await crud.crud_lookup.create(db, obj_in=killed_status)


async def init_lookup_severity(db: AsyncSession) -> None:
    severity_levels = await crud.crud_lookup.get_multi_by_type(
        db, type=settings.LOOKUP_TYPE_SEVERITY_LEVEL)
    if len(severity_levels) != 3:
        low_level = schemas.LookupCreate(
            id=5,
            type=settings.LOOKUP_TYPE_SEVERITY_LEVEL,
            name="LOW",
            description="Low severity level"
        )
        await crud.crud_lookup.create(db, obj_in=low_level)
        medium_level = schemas.LookupCreate(
            id=6,
            type=settings.LOOKUP_TYPE_SEVERITY_LEVEL,
            name="MEDIUM",
            description="Medium severity level"
        )
        await crud.crud_lookup.create(db, obj_in=medium_level)
        high_level = schemas.LookupCreate(
            id=7,
            type=settings.LOOKUP_TYPE_SEVERITY_LEVEL,
            name="HIGH",
            description="High severity level"
        )
        await crud.crud_lookup.create(db, obj_in=high_level)


async def init_lookup_vulnerability_type(db: AsyncSession) -> None:
    vuln_types = await crud.crud_lookup.get_multi_by_type(
        db, type=settings.LOOKUP_TYPE_VULNERABILITY_TYPE)
    if len(vuln_types) != 1:
        xss_type = schemas.LookupCreate(
            id=8,
            type=settings.LOOKUP_TYPE_VULNERABILITY_TYPE,
            name="XSS",
            description="Cross site scripting vulnerability (XSS)"
        )
        await crud.crud_lookup.create(db, obj_in=xss_type)


async def init() -> None:
    async with AsyncSessionLocal() as db:
        # await init_admin(db)
        # await init_user(db)
        await init_lookup_status(db)
        # await init_lookup_severity(db)
        # await init_lookup_vulnerability_type(db)


async def main() -> None:
    logger.info("Creating initial data")
    await init()
    logger.info("Initial data created")

if __name__ == "__main__":
    asyncio.run(main())
