import os
import asyncio
from redis.asyncio import Redis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

async def get_cached(key: str):
    return await redis.get(key)

async def set_cache(key: str, value: str, expire: int = 300):
    """Set cache with expiration in seconds"""
    await redis.set(key, value, ex=expire)
