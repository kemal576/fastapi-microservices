from pydantic import BaseModel, validator

from src.utils.hash import get_password_hash


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str

    class Config:
        validate_assignment = True

    @validator('password')
    def hash_password(cls, password):
        return get_password_hash(password)


class UserUpdate(UserCreate):
    pass


class User(UserBase):
    id: int
    # orders: list[Order] = []
    # notifications: list[UserNotification] = []

    class Config:
        orm_mode = True
