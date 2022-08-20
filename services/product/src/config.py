import os


class Settings:
    API_KEY = os.getenv("API_KEY")

    REDIS_HOST = os.getenv("REDIS_HOST")

    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
    PRODUCT_DB = os.getenv("PRODUCT_DB")

    POSTGRES_CONN_STR = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:5432/{PRODUCT_DB}"
