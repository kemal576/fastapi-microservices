from typing import AsyncGenerator
from faker import Faker
import pytest
from httpx import AsyncClient
from src.main import app

faker = Faker()


@pytest.fixture
async def client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://localhost") as client:
        yield client


@pytest.fixture
def anyio_backend():
    return 'asyncio'


async def override_auth(username: str = "test_username"):
    return username
