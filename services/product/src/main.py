import asyncio
import redis
from fastapi import FastAPI
from src.config import Settings
from src.events.event import start_consuming
from src.routers import product

app = FastAPI()
app.include_router(product.router)


@app.on_event("startup")
async def startup_event():
    r = redis.Redis(Settings.REDIS_HOST, decode_responses=True)
    asyncio.create_task(start_consuming(r))
