from fastapi import APIRouter
from fastapi import Depends

from auth.services import AuthService

router = APIRouter()


@router.get('/me')
def auth(auth_service: AuthService = Depends()):
    user = auth_service.authenticate()
    return user.email
