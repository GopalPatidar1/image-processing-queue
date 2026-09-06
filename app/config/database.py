from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from app.core.custom_exception import CustomException
from fastapi import status
from app.config.secretes import secretes
from sqlalchemy.exc import SQLAlchemyError

if not secretes.DB_URL:
    raise RuntimeError("DB_URL environment variable is not set")

class Base(DeclarativeBase):
    pass

engine = create_async_engine(
    secretes.DB_URL,
    pool_pre_ping=True,
    # echo=True
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)

async def get_db():
    try:
      async with SessionLocal() as db:
        yield db
    except SQLAlchemyError:
        raise CustomException(status.HTTP_503_SERVICE_UNAVAILABLE, "Database service is temporarily unavailable")
        
