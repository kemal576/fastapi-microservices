from typing import Callable
import pytest
from faker import Faker

faker = Faker()


@pytest.fixture
def user_create_data() -> Callable:
    def generate_payload(**kwargs: None) -> dict:
        return {
            "username": kwargs.get("username") or faker.pystr(max_chars=10),
            "password": kwargs.get("password") or faker.pystr(max_chars=10)
        }

    return generate_payload


@pytest.fixture
def order_create_data() -> Callable:
    def generate_payload(**kwargs: None) -> dict:
        return {
            "product_id": kwargs.get("product_id") or faker.pyint(),
            "user_id": kwargs.get("user_id") or faker.pyint(min_value=1, max_value=5),
            "quantity": kwargs.get("quantity") or faker.pyfloat(),
            "price": kwargs.get("price") or faker.pyfloat()
        }

    return generate_payload


@pytest.fixture
def notification_create_data() -> Callable:
    def generate_payload(**kwargs: None) -> dict:
        return {
            "user_id": kwargs.get("user_id") or faker.pyint(min_value=1, max_value=5),
            "message": kwargs.get("message") or faker.pystr(max_chars=30)
        }

    return generate_payload
