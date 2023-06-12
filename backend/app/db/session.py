from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_async_engine(
    f"mysql+aiomysql://{settings.MARIADB_USER}:{settings.MARIADB_PASSWORD}@localhost/{settings.MARIADB_DATABASE}", echo=True
)  # use pymysql when it is sync engine

# Create a sessionmaker
AsyncSessionLocal = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
