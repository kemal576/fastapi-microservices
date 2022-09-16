import random
from typing import Callable
import pytest
from fastapi import Depends
from httpx import AsyncClient
from src.dependencies import get_db
from src.events.order import OrderEvents
from src.main import app
from src.models.order import Order
from src.services.user import UserService
from src.utils.auth import basic_auth
from tests.conftest import override_auth
from tests.test_db import override_get_db
from tests.factories.factories import order_create_data


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[basic_auth] = override_auth


@pytest.mark.anyio
async def test_create_order_success(client: AsyncClient, order_create_data: Callable, monkeypatch):
    # Mocking order creation event
    async def mock_create_event(self, _):
        print("Event creation process mocked.")

    monkeypatch.setattr(OrderEvents, "produce_event", mock_create_event)

    # given
    payload = order_create_data()

    async def override_auth_update(id: int = payload.get("user_id"),
                                   user_service: UserService = Depends()):
        user = await user_service.get(id)
        return user.username

    app.dependency_overrides[basic_auth] = override_auth_update

    # when
    response = await client.post(url="/order/", json=payload)

    app.dependency_overrides[basic_auth] = override_auth

    # then
    assert response.status_code == 201


@pytest.mark.anyio
async def test_get_all_success(client: AsyncClient):

    # when
    response = await client.get(url="/order/")

    # then
    assert response.status_code == 200


# @pytest.mark.anyio
# async def test_get_all_fail(client: AsyncClient):
#
#     # when
#     response = await client.get(url="/order/")
#
#     # then
#     assert response.status_code == 404


@pytest.mark.anyio
async def test_get_order_success(client: AsyncClient):
    test_id = random.randint(1, 5)

    # when
    response = await client.get(url=f"/order/{test_id}")

    # then
    assert response.status_code == 200
    assert Order(**response.json()).id == test_id


@pytest.mark.anyio
async def test_get_order_fail(client: AsyncClient):

    # when
    response = await client.get(url="/order/0")

    # then
    assert response.status_code == 404


@pytest.mark.anyio
async def test_update_order_success(client: AsyncClient):
    test_id = random.randint(1, 5)

    order_update_dict = {"price": 150, "quantity": 50}

    # when
    response = await client.put(url=f"/order/{test_id}", json=order_update_dict)
    updated_order = Order(**response.json())
    # then
    assert response.status_code == 200
    assert updated_order.price == order_update_dict.get("price")
    assert updated_order.quantity == order_update_dict.get("quantity")


@pytest.mark.anyio
async def test_update_order_fail(client: AsyncClient):
    order_update = {"price": 150, "quantity": 50}
    # when
    response = await client.put(url="/order/0", json=order_update)

    # then
    assert response.status_code == 404


@pytest.mark.anyio
async def test_patch_success(client: AsyncClient):
    test_id = random.randint(1, 5)

    payload = {"price": 180}

    # when
    response = await client.patch(url=f"/order/{test_id}", json=payload)

    # then
    assert response.status_code == 200
    assert Order(**response.json()).price == payload.get("price")


@pytest.mark.anyio
async def test_patch_fail(client: AsyncClient):
    test_id = random.randint(1, 5)

    payload = {"not_real_variable": 180}

    # when
    response = await client.patch(url=f"/order/{test_id}", json=payload)

    # then
    assert response.status_code == 422


@pytest.mark.anyio
async def test_delete_success(client: AsyncClient):
    app.dependency_overrides[basic_auth] = override_auth

    test_id = random.randint(1, 5)
    response = await client.delete(url=f"/users/{test_id}")
    assert response.status_code == 204


