from fastapi import Depends
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.dependencies import get_db
from src.models.user import User
from src.schemas.user import UserCreate


class UserService:
    def __init__(self, db: AsyncSession = Depends(get_db)) -> None:
        self.db = db

    async def create(self, user: UserCreate) -> User:
        db_user = User(**user.dict())
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def update(self, db_user: User, user_update: dict) -> User:
        stmt = update(User).where(User.id == db_user.id).values(**user_update)
        await self.db.execute(stmt)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def get(self, user_id: int) -> User:
        return await self.db.get(User, user_id, populate_existing=True)

    async def get_by_username(self, username: str) -> User:
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalars().first()

    async def get_all(self) -> list[User]:
        result = await self.db.scalars(statement=select(User))
        return result.all()

    async def delete(self, user: User):
        await self.db.delete(user)
        await self.db.commit()

