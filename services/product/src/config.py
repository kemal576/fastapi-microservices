import os


class Settings:
    API_KEY = os.getenv("API_KEY")

    REDIS_HOST = os.getenv("REDIS_HOST")

    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
    PRODUCT_DB = os.getenv("PRODUCT_DB")
    TEST_DB = os.getenv("TEST_DB")

    CONN_STR = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:5432"
    PRODUCT_CONN_STR = f"{CONN_STR}/{PRODUCT_DB}"
    TEST_CONN_STR = f"{CONN_STR}/{TEST_DB}"
