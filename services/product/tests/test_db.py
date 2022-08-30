import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from src.config import Settings
from src.database import Base

engine = create_async_engine(url=Settings.TEST_CONN_STR, poolclass=NullPool)
TestingSessionLocal = sessionmaker(bind=engine,
                                   expire_on_commit=False,
                                   class_=AsyncSession,
                                   future=True)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(async_main())


async def override_get_db() -> AsyncGenerator:
    async with TestingSessionLocal() as session:
        yield session
