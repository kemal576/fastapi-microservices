from pydantic import BaseModel


# class UserNotificationBase(BaseModel):
#     message: str
#
#
# class UserNotificationCreate(UserNotificationBase):
#     user_id: int
#
#
# class UserNotificationUpdate(UserNotificationBase):
#     pass


class UserNotification(BaseModel):
    id: int
    message: str
    user_id: int

    class Config:
        orm_mode = True
