from typing import AsyncGenerator
import pytest
from fastapi import HTTPException
from httpx import AsyncClient
from src.main import app
from src.models.product import Product
from src.services.product import ProductService

API_KEY_HEADER = {"X-API-KEY": "12345"}

product_dict: dict = {"name": "test_name", "quantity": 20, "price": 30}
product = Product(**product_dict)
product.id = 1


@pytest.fixture
async def client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://localhost") as client:
        yield client


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.mark.anyio
async def test_create_product_success(client: AsyncClient, monkeypatch):
    async def mock_create(self, _):
        return product

    monkeypatch.setattr(ProductService, "create", mock_create)

    # when
    response = await client.post(url="/products/", json=product_dict, headers=API_KEY_HEADER)

    # then
    assert response.status_code == 201


@pytest.mark.anyio
async def test_get_all_success(client: AsyncClient, monkeypatch):
    async def mock_get_all(self):
        return [product]

    monkeypatch.setattr(ProductService, "get_all", mock_get_all)

    # when
    response = await client.get(url="/products/", headers=API_KEY_HEADER)

    # then
    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_all_fail(client: AsyncClient, monkeypatch):
    async def mock_get_all(self):
        return []

    monkeypatch.setattr(ProductService, "get_all", mock_get_all)

    # when
    response = await client.get(url="/products/", headers=API_KEY_HEADER)

    # then
    assert response.status_code == 404


@pytest.mark.anyio
async def test_get_product_success(client: AsyncClient, monkeypatch):
    async def mock_get(self, _):
        return product

    monkeypatch.setattr(ProductService, "get", mock_get)

    # when
    response = await client.get(url="/products/1", headers=API_KEY_HEADER)

    # then
    assert response.status_code == 200
    assert Product(**response.json()).id == 1


@pytest.mark.anyio
async def test_get_product_fail(client: AsyncClient, monkeypatch):
    async def mock_get(self, _):
        return None

    monkeypatch.setattr(ProductService, "get", mock_get)

    # when
    response = await client.get(url="/products/1", headers=API_KEY_HEADER)

    # then
    assert response.status_code == 404


@pytest.mark.anyio
async def test_update_product_success(client: AsyncClient, monkeypatch):
    async def mock_update(self, _, x):
        return product

    monkeypatch.setattr(ProductService, "update", mock_update)

    # when
    response = await client.put(url="/products/1", json=product_dict, headers=API_KEY_HEADER)

    # then
    assert response.status_code == 200


@pytest.mark.anyio
async def test_update_product_fail(client: AsyncClient, monkeypatch):
    async def mock_update(self, _, x):
        raise HTTPException(status_code=404, detail="Product not found")

    monkeypatch.setattr(ProductService, "update", mock_update)

    # when
    response = await client.put(url="/products/1", json=product_dict, headers=API_KEY_HEADER)

    # then
    assert response.status_code == 404


@pytest.mark.anyio
async def test_patch_quantity_success(client: AsyncClient, monkeypatch):
    async def mock_patch_quantity(self, _, x):
        return product

    monkeypatch.setattr(ProductService, "update_quantity", mock_patch_quantity)

    payload = {"quantity": 15}

    # when
    response = await client.patch(url="/products/1", json=payload, headers=API_KEY_HEADER)

    # then
    assert response.status_code == 200
    assert Product(**response.json()).quantity == product.quantity


@pytest.mark.anyio
async def test_patch_auth_fail(client: AsyncClient, monkeypatch):
    # when
    response = await client.patch(url="/products/1",
                                  json={"test": "test"},
                                  headers={"X-API-KEY": "wrong_key_123"})

    # then
    assert response.status_code == 401
