from typing import AsyncGenerator
from src.database import session_factory


async def get_db() -> AsyncGenerator:
    async with session_factory() as session:
        yield session
