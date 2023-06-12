from sqlmodel import Session, SQLModel, create_async_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_async_engine(
    f"mysql+pymysql://{settings.MARIADB_USER}:{settings.MARIADB_PASSWORD}@localhost/{settings.MARIADB_DATABASE}", echo=True
)

# Create a sessionmaker
AsyncSessionLocal = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
