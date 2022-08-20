from pydantic import BaseModel


class OrderBase(BaseModel):
    quantity: float
    price: float


class OrderCreate(OrderBase):
    product_id: int
    user_id: int


class OrderUpdate(OrderBase):
    pass


class Order(OrderCreate):
    id: int

    class Config:
        orm_mode = True
