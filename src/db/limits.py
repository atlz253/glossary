import asyncio
from . import POOL_SIZE
from functools import wraps

db_semaphore = asyncio.Semaphore(POOL_SIZE)


def limit_db_concurrency(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with db_semaphore:
            return await func(*args, **kwargs)
    return wrapper


__all__ = ["limit_db_concurrency"]
