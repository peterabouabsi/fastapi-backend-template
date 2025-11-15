from asyncio import iscoroutine
from typing import Callable

async def resolve_key(fn: Callable[..., str], *args, **kwargs) -> str:
    result = fn(*args, **kwargs)
    if iscoroutine(result):
        result = await result
    return result