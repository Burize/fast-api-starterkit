from fastapi import APIRouter
from store.controllers import order_router

api_router = APIRouter()
api_router.include_router(order_router, prefix='/order')
