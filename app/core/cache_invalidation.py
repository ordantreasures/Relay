from app.core.cache import redis
from typing import Optional

async def invalidate_feed_cache(user_id: Optional[int] = None):
    """Invalidate feed cache"""
    keys = await redis.keys("feed:*")
    if keys:
        await redis.delete(*keys)

async def invalidate_trending_cache():
    """Invalidate trending cache"""
    keys = await redis.keys("trending:*")
    if keys:
        await redis.delete(*keys)

async def invalidate_user_cache(user_id: int):
    """Invalidate user-specific cache"""
    keys = await redis.keys(f"user:{user_id}:*")
    if keys:
        await redis.delete(*keys)