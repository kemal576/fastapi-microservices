from typing import AsyncGenerator
import pytest
from fastapi import HTTPException
from httpx import AsyncClient
from src.events.order import OrderEvents
from src.main import app
from src.models.order import Order
from src.models.user import User
from src.schemas.order import OrderCreate, OrderUpdate, OrderPriceUpdate
from src.services.order import OrderService
from src.services.user import UserService
from src.services.user_notification import UserNotificationService
from src.utils.auth import basic_auth

order_dict: dict = {"product_id": 1, "user_id": 1, "quantity": 30, "price": 200}
order_example = Order(id=1, **order_dict)


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
async def test_create_order_success(client: AsyncClient, monkeypatch):
    async def mock_get(self, user_id):
        return User(id=user_id, username="test_username")

    async def mock_create_order(self, order: OrderCreate):
        return Order(id=1, **order.dict())

    async def mock_create_notification(self, x, y):
        print("Notification creation process mocked.")

    async def mock_create_event(self, x):
        print("Event creation process mocked.")

    monkeypatch.setattr(UserService, "get", mock_get)
    monkeypatch.setattr(OrderService, "create", mock_create_order)
    monkeypatch.setattr(UserNotificationService, "create", mock_create_notification)
    monkeypatch.setattr(OrderEvents, "produce_event", mock_create_event)

    # when
    response = await client.post(url="/order/", json=order_dict)

    # then
    assert response.status_code == 201


@pytest.mark.anyio
async def test_get_all_success(client: AsyncClient, monkeypatch):
    async def mock_get_all(self):
        return [order_example]

    monkeypatch.setattr(OrderService, "get_all", mock_get_all)

    # when
    response = await client.get(url="/order/")

    # then
    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_all_fail(client: AsyncClient, monkeypatch):
    async def mock_get_all(self):
        return []

    monkeypatch.setattr(OrderService, "get_all", mock_get_all)

    # when
    response = await client.get(url="/order/")

    # then
    assert response.status_code == 404


@pytest.mark.anyio
async def test_get_order_success(client: AsyncClient, monkeypatch):
    async def mock_get(self, order_id: int):
        order = Order(id=order_id, **order_dict)
        return order

    monkeypatch.setattr(OrderService, "get", mock_get)

    # when
    response = await client.get(url="/order/1")

    # then
    assert response.status_code == 200
    assert Order(**response.json()).id == order_example.id


@pytest.mark.anyio
async def test_get_order_fail(client: AsyncClient, monkeypatch):
    async def mock_get(self, _):
        return None

    monkeypatch.setattr(OrderService, "get", mock_get)

    # when
    response = await client.get(url="/order/1")

    # then
    assert response.status_code == 404


@pytest.mark.anyio
async def test_update_order_success(client: AsyncClient, monkeypatch):
    async def mock_get(self, order_id: int):
        order = Order(id=order_id, **order_dict)
        return order

    async def mock_update(self, db_order: Order, order: OrderUpdate):
        db_order.quantity = order.quantity
        db_order.price = order.price
        return db_order

    monkeypatch.setattr(OrderService, "get", mock_get)
    monkeypatch.setattr(OrderService, "update", mock_update)

    order_update = {"price": 150, "quantity": 50}

    # when
    response = await client.put(url="/order/1", json=order_update)

    # then
    assert response.status_code == 200


@pytest.mark.anyio
async def test_update_order_fail(client: AsyncClient, monkeypatch):
    async def mock_get(self, _):
        raise HTTPException(status_code=404, detail="Order not found")

    monkeypatch.setattr(OrderService, "get", mock_get)
    order_update = {"price": 150, "quantity": 50}
    # when
    response = await client.put(url="/order/1", json=order_update)

    # then
    assert response.status_code == 404


@pytest.mark.anyio
async def test_patch_price_success(client: AsyncClient, monkeypatch):
    async def mock_get(self, user_id: int):
        return Order(id=user_id, **order_dict)

    async def mock_patch_price(self, db_order: Order, order: OrderPriceUpdate):
        db_order.price = order.price
        return db_order

    monkeypatch.setattr(OrderService, "get", mock_get)
    monkeypatch.setattr(OrderService, "update_price", mock_patch_price)

    payload = {"price": 180}

    # when
    response = await client.patch(url="/order/1", json=payload)

    # then
    assert response.status_code == 200
    assert Order(**response.json()).price == payload.get("price")
