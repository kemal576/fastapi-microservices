from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.dependencies import get_db
from src.models.product import Product
from src.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, db: AsyncSession = Depends(get_db)) -> None:
        self.db = db

    async def create(self, product: ProductCreate):
        db_product = Product(name=product.name, quantity=product.quantity, price=product.price)
        self.db.add(db_product)
        await self.db.commit()
        await self.db.refresh(db_product)
        return db_product

    async def update(self, product_id: int, product: ProductUpdate):
        db_product: Product = await self.get(product_id)
        if db_product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        db_product.name = product.name
        db_product.price = product.price
        db_product.quantity = product.quantity

        await self.db.commit()
        return db_product

    async def update_quantity(self, product_id: int, quantity: float):
        db_product: Product = await self.get(product_id)
        if db_product is None:
            raise HTTPException(status_code=404, detail="Product not found")

        db_product.quantity = quantity

        await self.db.commit()
        return db_product

    async def get(self, product_id: int):
        return await self.db.get(Product, product_id)

    async def get_all(self):
        result = await self.db.scalars(statement=select(Product))
        return result.all()

    async def delete(self, product: Product):
        await self.db.delete(product)
        await self.db.commit()
