from sqlalchemy.ext.asyncio import AsyncSession

from src.models.order import Order
from src.models.user import User
from src.models.user_notification import UserNotification

users_test_data = [
    {
        "username": "JohnDoe",
        "password": "d98yfs9hfs8dhfs08dfsd8fh"
    },
    {
        "username": "KemalŞahin",
        "password": "09w4jtpmfw9eufj0qw9jemfksdfn"
    },
    {
        "username": "JoeBiden",
        "password": "bg8yh5ıun4.as8d809ajsndıansd"
    },
    {
        "username": "OgünHeper",
        "password": "3298hwuefn9hweoıfnodf9ufd98gy"
    },
    {
        "username": "GökhanKaraboğa",
        "password": "092u30jfnd0f98h408hfwhf0h8f028"
    }
]

orders_test_data = [
    {
        "product_id": 1,
        "user_id": 1,
        "quantity": 10,
        "price": 100
    },
    {
        "product_id": 2,
        "user_id": 2,
        "quantity": 20,
        "price": 200
    },
    {
        "product_id": 3,
        "user_id": 3,
        "quantity": 30,
        "price": 300
    },
    {
        "product_id": 4,
        "user_id": 4,
        "quantity": 40,
        "price": 400
    },
    {
        "product_id": 5,
        "user_id": 5,
        "quantity": 50,
        "price": 500
    }
]

ntf_test_data = [
    {
        "user_id": 1,
        "message": "Hello 1"
    },
    {
        "user_id": 2,
        "message": "Hello 2"
    },
    {
        "user_id": 3,
        "message": "Hello 3"
    },
    {
        "user_id": 4,
        "message": "Hello 4"
    },
    {
        "user_id": 5,
        "message": "Hello 5"
    }
]


async def seed_database(session: AsyncSession):
    users: list[User] = []
    for user_json in users_test_data:
        users.append(User(**user_json))
    session.add_all(users)

    orders: list[Order] = []
    for order_json in orders_test_data:
        orders.append(Order(**order_json))
    session.add_all(orders)

    notifications: list[UserNotification] = []
    for ntf in ntf_test_data:
        notifications.append(UserNotification(**ntf))
    session.add_all(notifications)

    await session.commit()
