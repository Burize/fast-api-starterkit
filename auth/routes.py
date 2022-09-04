from fastapi import APIRouter
from auth.controllers import auth_router

api_router = APIRouter(prefix='/auth')
api_router.include_router(auth_router, prefix="/user")
