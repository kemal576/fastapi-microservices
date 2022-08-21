from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from src.events.event import produce_event
from src.services.order import OrderService
from src.schemas.order import Order, OrderCreate, OrderUpdate, OrderPriceUpdate
from src.services.user import UserService
from src.services.user_notification import UserNotificationService
from fastapi import BackgroundTasks
from src.utils.auth import basic_auth

router = APIRouter(prefix="/order", tags=["Order"])


@router.post("/", response_model=Order)
async def create_order(order: OrderCreate,
                       background_tasks: BackgroundTasks,
                       service: OrderService = Depends(),
                       notification_service: UserNotificationService = Depends(),
                       user_service: UserService = Depends(),
                       current_username: str = Depends(basic_auth)):

    user = await user_service.get(order.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found!")

    if current_username != user.username:
        raise HTTPException(status_code=403, detail="You can't create order for other users.")

    db_order = await service.create(order)

    message = {"product_id": db_order.product_id, "quantity": db_order.quantity}
    background_tasks.add_task(produce_event, "order_created", message)

    notification = f"Your order({db_order.id}) has successfully been created."
    background_tasks.add_task(notification_service.create, user, notification)
    return db_order


@router.put("/{order_id}", response_model=Order)
async def update_order(order_id: int,
                       order: OrderUpdate,
                       service: OrderService = Depends(),
                       _: str = Depends(basic_auth)):

    db_order = await service.get(order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found!")

    return await service.update(db_order=db_order, order=order)


@router.patch("/{order_id}", response_model=Order)
async def patch_order(order_id: int,
                      order: OrderPriceUpdate,
                      service: OrderService = Depends(),
                      _: str = Depends(basic_auth)):

    db_order = await service.get(order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found!")

    return await service.update_price(db_order=db_order, order=order)


@router.get("/", response_model=list[Order])
async def get_all(service: OrderService = Depends(),
                  _: str = Depends(basic_auth)):

    db_orders = await service.get_all()
    if len(db_orders) == 0:
        raise HTTPException(status_code=404, detail="Orders not found.")
    return db_orders


@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: int,
                    service: OrderService = Depends(),
                    _: str = Depends(basic_auth)):

    db_order = await service.get(order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int,
                       service: OrderService = Depends(),
                       _: str = Depends(basic_auth)):

    db_order = await service.get(order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    await service.delete(db_order)
