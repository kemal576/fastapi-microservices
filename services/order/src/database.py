from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config import Settings

engine = create_async_engine(url=Settings.ORDER_CONN_STR)
session_factory = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession, future=True)
Base = declarative_base()
