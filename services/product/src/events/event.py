import asyncio
import redis
from src.config import Settings
from src.events.order import OrderEvents


async def produce(stream_key: str, msg: dict):
    r = redis.Redis(host=Settings.REDIS_HOST, decode_responses=True)
    job_id = r.xadd(stream_key, msg)
    print(f"Created job {job_id}:")


async def start_consuming(r: redis.Redis):
    while True:
        results = r.xread(streams={"order_created": "$"}, count=1, block=5000)

        for result in results:
            if result[0] == "order_created":
                # job_id = result[1][0][0]
                message = result[1][0][1]
                await OrderEvents.order_created(message)
        await asyncio.sleep(0.5)
