from app.core.config import settings
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

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
