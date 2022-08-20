from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.dependencies import get_db
from src.models.user_notification import UserNotification
from src.services.user import UserService


class UserNotificationService:
    def __init__(self,
                 db: AsyncSession = Depends(get_db),
                 user_service: UserService = Depends()) -> None:
        self.db = db
        self.user_service = user_service

    async def create(self, user_id: int, message: str):
        user = await self.user_service.get(user_id)

        msg_with_usr = f"Hello {user.username}! {message}"
        db_notification = UserNotification(message=msg_with_usr, user_id=user_id)

        self.db.add(db_notification)
        await self.db.commit()

    async def get(self, notification_id: int) -> UserNotification:
        return await self.db.get(UserNotification, notification_id)

    async def get_by_user_id(self, user_id: int) -> list[UserNotification]:
        stmt = select(UserNotification).where(UserNotification.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_all(self,) -> list[UserNotification]:
        result = await self.db.scalars(select(UserNotification))
        return result.all()

    async def delete(self, notification: UserNotification):
        await self.db.delete(notification)
        await self.db.commit()
