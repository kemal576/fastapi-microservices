from pydantic import BaseModel


class ProductQuantityUpdate(BaseModel):
    quantity: float


class ProductCreate(ProductQuantityUpdate):
    name: str
    price: float


class ProductUpdate(ProductCreate):
    pass


class Product(ProductCreate):
    id: int

    class Config:
        orm_mode = True


