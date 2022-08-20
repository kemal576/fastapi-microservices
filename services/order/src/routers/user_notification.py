from fastapi import APIRouter, Depends, HTTPException
from src.schemas.user_notification import UserNotification
from src.services.user import UserService
from src.services.user_notification import UserNotificationService
from src.utils.auth import basic_auth

router = APIRouter(prefix="/notifications", tags=["User Notifications"])


@router.get("/", response_model=list[UserNotification])
async def get_all(service: UserNotificationService = Depends(),
                  _: str = Depends(basic_auth)):

    db_notification = await service.get_all()
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notifications not found.")
    return db_notification


@router.get("/{notification_id}", response_model=UserNotification)
async def get_notification(notification_id: int,
                           service: UserNotificationService = Depends(),
                           _: str = Depends(basic_auth)):

    db_notification = await service.get(notification_id)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification


@router.get("/{user_id}", response_model=list[UserNotification])
async def get_by_user_id(user_id: int,
                         service: UserNotificationService = Depends(),
                         user_service: UserService = Depends(),
                         current_username: str = Depends(basic_auth)):
    user = await user_service.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    if current_username != user.username:
        raise HTTPException(status_code=403, detail="You can't see other users notifications!")

    db_notifications = await service.get_by_user_id(user_id)
    if len(db_notifications) == 0:
        raise HTTPException(status_code=404, detail="This user dont have any notification.")
    return db_notifications
