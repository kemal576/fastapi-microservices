from typing import AsyncGenerator
import pytest
from fastapi import HTTPException
from httpx import AsyncClient
from src.main import app
from src.models.user import User
from src.schemas.user import UserUpdate, UserBase, UserCreate
from src.services.user import UserService
from src.utils.auth import basic_auth

user_dict: dict = {"username": "test_username", "password": "test_pass"}
user_example = User(id=1, **user_dict)


async def override_auth(username: str = "test_username"):
    return username

app.dependency_overrides[basic_auth] = override_auth


@pytest.fixture
async def client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://localhost") as client:
        yield client


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.mark.anyio
async def test_create_user_success(client: AsyncClient, monkeypatch):
    async def mock_get_by_username(self, username: str):
        return None

    async def mock_create(self, user: UserCreate):
        return User(id=1, **user.dict())

    monkeypatch.setattr(UserService, "get_by_username", mock_get_by_username)
    monkeypatch.setattr(UserService, "create", mock_create)

    # when
    response = await client.post(url="/users/", json=user_dict)

    # then
    assert response.status_code == 201


@pytest.mark.anyio
async def test_get_all_success(client: AsyncClient, monkeypatch):
    async def mock_get_all(self):
        return [user_example]

    monkeypatch.setattr(UserService, "get_all", mock_get_all)

    # when
    response = await client.get(url="/users/")

    # then
    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_all_fail(client: AsyncClient, monkeypatch):
    async def mock_get_all(self):
        return []

    monkeypatch.setattr(UserService, "get_all", mock_get_all)

    # when
    response = await client.get(url="/users/")

    # then
    assert response.status_code == 404


@pytest.mark.anyio
async def test_get_user_success(client: AsyncClient, monkeypatch):
    async def mock_get(self, user_id: int):
        user = User(id=user_id, **user_dict)
        return user

    monkeypatch.setattr(UserService, "get", mock_get)

    # when
    response = await client.get(url="/users/1")

    # then
    assert response.status_code == 200
    assert User(**response.json()).id == user_example.id


@pytest.mark.anyio
async def test_get_user_fail(client: AsyncClient, monkeypatch):
    async def mock_get(self, _):
        return None

    monkeypatch.setattr(UserService, "get", mock_get)

    # when
    response = await client.get(url="/users/1")

    # then
    assert response.status_code == 404


@pytest.mark.anyio
async def test_update_user_success(client: AsyncClient, monkeypatch):
    async def mock_get(self, user_id: int):
        user = User(id=user_id, **user_dict)
        return user

    async def mock_update(self, db_user: User, user_update: UserUpdate):
        return User(id=db_user.id, **user_update.dict())

    async def mock_get_by_username(self, username: str):
        return None

    monkeypatch.setattr(UserService, "get", mock_get)
    monkeypatch.setattr(UserService, "update", mock_update)
    monkeypatch.setattr(UserService, "get_by_username", mock_get_by_username)

    user_update_dict = {"username": "test_username_2", "password": "test_pass"}

    # when
    response = await client.put(url="/users/1", json=user_update_dict)

    # then
    assert response.status_code == 200


@pytest.mark.anyio
async def test_update_user_fail(client: AsyncClient, monkeypatch):
    async def mock_get(self, _):
        raise HTTPException(status_code=404, detail="User not found")

    monkeypatch.setattr(UserService, "get", mock_get)
    user_update = {"username": "test_name", "password": "test_pass"}
    # when
    response = await client.put(url="/users/1", json=user_update)

    # then
    assert response.status_code == 404


@pytest.mark.anyio
async def test_patch_username_success(client: AsyncClient, monkeypatch):
    async def mock_get(self, user_id: int):
        return User(id=user_id, **user_dict)

    async def mock_patch_username(self, db_user: User, user: UserBase):
        db_user.username = user.username
        return db_user

    monkeypatch.setattr(UserService, "get", mock_get)
    monkeypatch.setattr(UserService, "update_username", mock_patch_username)

    payload = {"username": "test_username_2"}

    # when
    response = await client.patch(url="/users/1", json=payload)

    # then
    assert response.status_code == 200
    assert User(**response.json()).username == payload.get("username")


@pytest.mark.anyio
async def test_basic_auth_fail(client: AsyncClient):
    async def override_auth_fail(username: str = ""):
        raise HTTPException(status_code=401, detail="forbidden")

    app.dependency_overrides[basic_auth] = override_auth_fail

    response = await client.get(url="/users/")
    assert response.status_code == 401

