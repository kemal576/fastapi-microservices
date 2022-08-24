from typing import AsyncGenerator
import pytest
from httpx import AsyncClient
from src.main import app
from src.models.user import User
from src.models.user_notification import UserNotification
from src.services.user import UserService
from src.services.user_notification import UserNotificationService
from src.utils.auth import basic_auth

ntf_dict: dict = {"user_id": 1, "message": "test_message"}
ntf_example = UserNotification(id=1, **ntf_dict)


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
async def test_get_all_success(client: AsyncClient, monkeypatch):
    async def mock_get_all(self):
        return [ntf_example]

    monkeypatch.setattr(UserNotificationService, "get_all", mock_get_all)

    # when
    response = await client.get(url="/notifications/")

    # then
    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_all_fail(client: AsyncClient, monkeypatch):
    async def mock_get_all(self):
        return []

    monkeypatch.setattr(UserNotificationService, "get_all", mock_get_all)

    # when
    response = await client.get(url="/notifications/")

    # then
    assert response.status_code == 404


# @pytest.mark.anyio
# async def test_get_by_user_id(client: AsyncClient, monkeypatch):
#     async def mock_get_by_user_id(self, user_id):
#         ntf = UserNotification(id=1, user_id=user_id)
#         return [ntf]
#
#     async def mock_get_user(self, user_id: int):
#         return User(id=user_id, username="test_username")
#
#     monkeypatch.setattr(UserService, "get", mock_get_user)
#     monkeypatch.setattr(UserNotificationService, "get_by_user_id", mock_get_by_user_id)
#
#     # when
#     response = await client.get(url="/notifications/", params={"user_id": 1})
#
#     # then
#     #print(response.json())
#     assert response.status_code == 200
#     # assert UserNotification(**response.json()[0]).user_id == ntf_example.id


@pytest.mark.anyio
async def test_get_ntf_success(client: AsyncClient, monkeypatch):
    async def mock_get(self, notification_id: int):
        return UserNotification(id=notification_id, **ntf_dict)

    monkeypatch.setattr(UserNotificationService, "get", mock_get)

    # when
    response = await client.get(url="/notifications/1")

    # then
    assert response.status_code == 200
    assert UserNotification(**response.json()).id == ntf_example.id


@pytest.mark.anyio
async def test_get_ntf_fail(client: AsyncClient, monkeypatch):
    async def mock_get(self, _):
        return None

    monkeypatch.setattr(UserNotificationService, "get", mock_get)

    # when
    response = await client.get(url="/notifications/1")

    # then
    assert response.status_code == 404
