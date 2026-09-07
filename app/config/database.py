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
from sqlalchemy.pool import NullPool

if not secretes.DB_URL:
    raise RuntimeError("DB_URL environment variable is not set")

class Base(DeclarativeBase):
    pass

engine_kwargs = {
    "pool_pre_ping": True,
}

if secretes.APP_ENV == "test":
    engine_kwargs["poolclass"] = NullPool # Use NullPool in tests to prevent asyncpg connections from # being reused across different pytest event loops.

engine = create_async_engine(
    secretes.DB_URL,
    **engine_kwargs,
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
        
