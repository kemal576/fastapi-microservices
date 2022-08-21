from pydantic import BaseModel


class OrderPriceUpdate(BaseModel):
    price: float


class OrderUpdate(OrderPriceUpdate):
    quantity: float


class OrderCreate(OrderUpdate):
    product_id: int
    user_id: int


class Order(OrderCreate):
    id: int

    class Config:
        orm_mode = True
