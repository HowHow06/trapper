import logging
from sqlalchemy.orm import Session
from app import crud, schemas
from app.core.config import settings
from app.db.session import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio


# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init_db(db: AsyncSession) -> None:
    user = await crud.crud_user.get_by_email_or_username(
        db, email=settings.FIRST_SUPERUSER_EMAIL, username=settings.FIRST_SUPERUSER_USERNAME)
    if not user:
        user_in = schemas.UserCreate(
            username=settings.FIRST_SUPERUSER_USERNAME,
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
        )
        user = await crud.crud_user.create(db, obj_in=user_in)


async def init() -> None:
    async with AsyncSessionLocal() as db:
        await init_db(db)


async def main() -> None:
    logger.info("Creating initial data")
    await init()
    logger.info("Initial data created")

if __name__ == "__main__":
    asyncio.run(main())
