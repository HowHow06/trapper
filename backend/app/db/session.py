from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


def get_db_url():
    return f"mysql+pymysql://{settings.MARIADB_USER}:{settings.MARIADB_PASSWORD}@{settings.MARIADB_SERVER}/{settings.MARIADB_DATABASE}"


def get_async_db_url():
    return f"mysql+aiomysql://{settings.MARIADB_USER}:{settings.MARIADB_PASSWORD}@{settings.MARIADB_SERVER}/{settings.MARIADB_DATABASE}"


async_engine = create_async_engine(
    get_async_db_url(), echo=settings.ENVIRONMENT == "dev"
)  # use pymysql when it is sync engine

# Create a sessionmaker
AsyncSessionLocal = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession)


sync_engine = create_engine(get_db_url(), pool_pre_ping=True)
SyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=sync_engine)
