from functools import wraps
from typing import Callable
from fastapi import HTTPException, Request
from app.core.cache import redis
import asyncio

def rate_limit(max_requests: int = 100, time_window: int = 60):
    """Rate limiting decorator"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract request from kwargs
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if not request:
                for key, value in kwargs.items():
                    if isinstance(value, Request):
                        request = value
                        break
            
            if not request:
                return await func(*args, **kwargs)
            
            # Use IP address as key
            ip = request.client.host if request.client else "unknown"
            endpoint = request.url.path
            key = f"rate_limit:{ip}:{endpoint}"
            
            # Check current count
            current = await redis.get(key)
            if current and int(current) >= max_requests:
                raise HTTPException(
                    status_code=429,
                    detail=f"Rate limit exceeded. Try again in {time_window} seconds"
                )
            
            # Increment counter
            pipeline = redis.pipeline()
            pipeline.incr(key)
            pipeline.expire(key, time_window)
            await pipeline.execute()
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator