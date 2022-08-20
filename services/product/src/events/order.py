from sqlalchemy.ext.asyncio import AsyncSession
from src.database import session_factory
from src.models.product import Product
from src.services.product import ProductService


class OrderEvents:
    @staticmethod
    async def order_created(message: dict):
        db: AsyncSession = session_factory()
        service = ProductService(db)

        product_id = int(message.get("product_id"))
        quantity = float(message.get("quantity"))
        if product_id and quantity is None:
            raise Exception(f"Order create event's message is not compatible -> {message}")

        product: Product = await service.get(product_id)
        await service.update(product_id, {"quantity": product.quantity-quantity})

        print("Order created event triggered. ->", message)
