from pydantic import BaseModel


class UserNotification(BaseModel):
    id: int
    message: str
    user_id: int

    class Config:
        orm_mode = True
