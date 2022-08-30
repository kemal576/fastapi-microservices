import pytest
from faker import Faker
from httpx import AsyncClient
from src.dependencies import get_db
from src.main import app
from src.models.product import Product
from tests.test_db import override_get_db

faker = Faker()
app.dependency_overrides[get_db] = override_get_db

product_dict: dict = {"name": "test_name", "quantity": 20, "price": 30}
product = Product(**product_dict)
product.id = 1


@pytest.mark.anyio
async def test_create_product_success(client: AsyncClient,
                                      internal_request_headers):
    # when
    response = await client.post(url="/products/", json=product_dict, headers=internal_request_headers)

    # then
    assert response.status_code == 201


@pytest.mark.anyio
async def test_get_all_success(client: AsyncClient,
                               internal_request_headers):

    # when
    response = await client.get(url="/products/", headers=internal_request_headers)

    # then
    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_product_success(client: AsyncClient,
                                   internal_request_headers):

    # when
    response = await client.get(url="/products/1", headers=internal_request_headers)

    # then
    assert response.status_code == 200
    assert Product(**response.json()).id == 1


@pytest.mark.anyio
async def test_get_product_fail(client: AsyncClient,
                                internal_request_headers):

    # when
    response = await client.get(url="/products/0", headers=internal_request_headers)

    # then
    assert response.status_code == 404


@pytest.mark.anyio
async def test_update_product_success(client: AsyncClient,
                                      internal_request_headers):

    # when
    response = await client.put(url="/products/1", json=product_dict, headers=internal_request_headers)

    # then
    assert response.status_code == 200


@pytest.mark.anyio
async def test_update_product_fail(client: AsyncClient,
                                   internal_request_headers):

    # when
    response = await client.put(url="/products/0", json=product_dict, headers=internal_request_headers)

    # then
    assert response.status_code == 404


@pytest.mark.anyio
async def test_patch_success(client: AsyncClient,
                             internal_request_headers):

    payload = {"quantity": 15, "name": "new name"}

    # when
    response = await client.patch(url="/products/1", json=payload, headers=internal_request_headers)

    # then
    print(response.json())
    assert response.status_code == 200
    assert Product(**response.json()).quantity == payload.get("quantity")


@pytest.mark.anyio
async def test_auth_fail(client: AsyncClient, internal_request_headers):
    wrong_key_header = {"X-API-KEY": faker.pystr(max_chars=10)}
    # when
    response = await client.patch(url="/products/1",
                                  json=product_dict,
                                  headers=wrong_key_header)

    # then
    assert response.status_code == 401
