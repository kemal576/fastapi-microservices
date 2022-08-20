import os


class Settings:
    REDIS_HOST = os.getenv("REDIS_HOST")

    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
    ORDER_DB = os.getenv("ORDER_DB")

    POSTGRES_CONN_STR = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:5432/{ORDER_DB}"
