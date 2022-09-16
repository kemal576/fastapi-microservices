import random
from typing import Callable

import pytest
from fastapi import Depends
from httpx import AsyncClient
from src.dependencies import get_db
from src.main import app
from src.models.user_notification import UserNotification
from src.services.user import UserService
from src.utils.auth import basic_auth
from tests.conftest import override_auth
from tests.test_db import override_get_db
from tests.factories.factories import notification_create_data


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[basic_auth] = override_auth


@pytest.mark.anyio
async def test_get_all_success(client: AsyncClient, notification_create_data: Callable):

    # when
    response = await client.get(url="/notifications/")

    # then
    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_by_user_id(client: AsyncClient, monkeypatch):
    test_id = random.randint(1, 5)
    async def override_auth_update(id: int = test_id,
                                   user_service: UserService = Depends()):
        user = await user_service.get(id)
        return user.username

    app.dependency_overrides[basic_auth] = override_auth_update
    # when
    response = await client.get(url="/notifications/", params={"user_id": test_id})

    app.dependency_overrides[basic_auth] = override_auth

    # then
    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_ntf_success(client: AsyncClient, notification_create_data: Callable):
    test_id = random.randint(1, 5)

    # when
    response = await client.get(url=f"/notifications/{test_id}")

    # then
    assert response.status_code == 200
    assert UserNotification(**response.json()).id == test_id


@pytest.mark.anyio
async def test_get_ntf_fail(client: AsyncClient):

    # when
    response = await client.get(url="/notifications/0")

    # then
    assert response.status_code == 404
