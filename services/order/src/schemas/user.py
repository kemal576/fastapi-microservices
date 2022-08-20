from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserCreate):
    pass


class User(UserBase):
    id: int
    # orders: list[Order] = []
    # notifications: list[UserNotification] = []

    class Config:
        orm_mode = True
