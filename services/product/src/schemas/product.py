from pydantic import BaseModel


class ProductBase(BaseModel):
    quantity: float
    name: str
    price: float


class ProductPatch(ProductBase):
    quantity: float | None = None
    name: str | None = None
    price: float | None = None


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True


