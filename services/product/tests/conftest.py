from typing import AsyncGenerator
from unittest import mock
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


@pytest.fixture(autouse=True)
def internal_request_headers():
    secret_key = faker.pystr(max_chars=10)

    request_headers = {
        "X-API-KEY": secret_key,
    }

    with mock.patch("src.utils.auth.Settings.API_KEY", secret_key):
        yield request_headers
