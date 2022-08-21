from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.dependencies import get_db
from src.models.order import Order
from src.schemas.order import OrderCreate, OrderUpdate, OrderPriceUpdate


class OrderService:
    def __init__(self, db: AsyncSession = Depends(get_db)) -> None:
        self.db = db

    async def create(self, order: OrderCreate):
        db_order = Order(**order.dict())
        self.db.add(db_order)
        await self.db.commit()
        await self.db.refresh(db_order)
        return db_order

    async def update(self, db_order: Order, order: OrderUpdate):
        db_order.quantity = order.quantity
        db_order.price = order.price

        await self.db.commit()
        return db_order

    async def update_price(self, db_order: Order, order: OrderPriceUpdate):
        db_order.price = order.price

        await self.db.commit()
        return db_order

    async def get(self, order_id: int):
        return await self.db.get(Order, order_id)

    async def get_all(self):
        result = await self.db.scalars(statement=select(Order))
        return result.all()

    async def delete(self, order: Order):
        await self.db.delete(order)
        await self.db.commit()
