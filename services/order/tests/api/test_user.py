import random
from typing import Callable
import pytest
from fastapi import HTTPException, Depends
from httpx import AsyncClient
from src.dependencies import get_db
from src.main import app
from src.models.user import User
from src.services.user import UserService
from src.utils.auth import basic_auth
from tests.conftest import override_auth
from tests.test_db import override_get_db
from tests.factories.factories import user_create_data

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[basic_auth] = override_auth


@pytest.mark.anyio
async def test_create_user_success(client: AsyncClient, user_create_data: Callable):
    # given
    payload = user_create_data()

    # when
    response = await client.post(url="/users/", json=payload)

    # then
    assert response.status_code == 201


@pytest.mark.anyio
async def test_get_all_success(client: AsyncClient):
    # when
    response = await client.get(url="/users/")

    # then
    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_user_success(client: AsyncClient):
    test_id = random.randint(1, 5)

    # when
    response = await client.get(url=f"/users/{test_id}")

    # then
    assert response.status_code == 200
    assert User(**response.json()).id == test_id


@pytest.mark.anyio
async def test_get_user_fail(client: AsyncClient):
    # when
    response = await client.get(url="/users/0")

    # then
    assert response.status_code == 404


@pytest.mark.anyio
async def test_update_user_success(client: AsyncClient, user_create_data: Callable):
    test_id = random.randint(1, 5)

    async def override_auth_update(id: int = test_id,
                                   user_service: UserService = Depends()):
        user = await user_service.get(id)
        return user.username

    app.dependency_overrides[basic_auth] = override_auth_update

    # given
    user_update_dict = user_create_data()

    # when
    response = await client.put(url=f"/users/{test_id}", json=user_update_dict)

    # then
    assert response.status_code == 200


@pytest.mark.anyio
async def test_update_user_fail(client: AsyncClient, user_create_data: Callable):
    async def override_auth_update(username: str = "not_real_username"):
        return username

    app.dependency_overrides[basic_auth] = override_auth_update

    user_update = user_create_data()
    # when
    response = await client.put(url=f"/users/1", json=user_update)

    # then
    assert response.status_code == 403


@pytest.mark.anyio
async def test_patch_success(client: AsyncClient):
    payload = {"username": "test_username_2"}

    # when
    response = await client.patch(url="/users/1", json=payload)

    # then
    assert response.status_code == 200
    assert User(**response.json()).username == payload.get("username")


@pytest.mark.anyio
async def test_basic_auth_fail(client: AsyncClient):
    async def override_auth_fail(_: str = ""):
        raise HTTPException(status_code=401, detail="forbidden")

    app.dependency_overrides[basic_auth] = override_auth_fail

    response = await client.get(url="/users/")
    assert response.status_code == 401


@pytest.mark.anyio
async def test_delete_success(client: AsyncClient):
    app.dependency_overrides[basic_auth] = override_auth

    test_id = random.randint(1, 5)
    response = await client.delete(url=f"/users/{test_id}")
    assert response.status_code == 204
