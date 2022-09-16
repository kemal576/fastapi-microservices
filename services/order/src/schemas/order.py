from pydantic import BaseModel


class OrderUpdate(BaseModel):
    price: float
    quantity: float


class OrderPatch(OrderUpdate):
    price: float | None = None
    quantity: float | None = None


class OrderCreate(OrderUpdate):
    product_id: int
    user_id: int


class Order(OrderCreate):
    id: int

    class Config:
        orm_mode = True
