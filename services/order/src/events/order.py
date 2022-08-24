import redis
from src.config import Settings


class OrderEvents:
    @staticmethod
    async def produce_event(stream_key: str, msg: dict):
        r = redis.Redis(host=Settings.REDIS_HOST, decode_responses=True)
        job_id = r.xadd(stream_key, msg)
        print(f"Created job {job_id}")
