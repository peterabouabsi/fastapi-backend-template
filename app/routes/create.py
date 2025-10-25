from typing import Callable

from fastapi import APIRouter

def create_api_router(*route_setups_fn: Callable[[APIRouter], None]) -> APIRouter:
    router = APIRouter()
    for setup_fn in route_setups_fn:
        setup_fn(router)
    return router