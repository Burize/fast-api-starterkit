from fastapi import APIRouter
from auth.controllers import auth_router
from auth.controllers import user_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix='/authenticate')
api_router.include_router(user_router, prefix='/user')
