from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    quantity: float
    price: float


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True


