from fastapi import FastAPI
from src.routers import user, order, user_notification

app = FastAPI()
app.include_router(user.router)
app.include_router(order.router)
app.include_router(user_notification.router)
