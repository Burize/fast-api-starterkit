from dataclasses import dataclass
from uuid import UUID

from fastapi import Response
from injector import inject

from auth.services import AuthService
from auth.services.auth_service import AuthenticateException
from core.api import APIRouter
from core.api import controller
from core.dependencies import get_user_id
from core.exceptions import exception_to_response

router = APIRouter()


@dataclass
class UserAuthenticateDTO:
    username: str
    password: str


@dataclass
class UserDTO:
    id: UUID
    email: str


@controller
class AuthController:
    @inject
    def __init__(self, auth_service: AuthService):
        self._auth_service = auth_service

    @router.post('/login', no_authetication=True)
    @exception_to_response(AuthenticateException, http_code=401)
    async def authenticate(self, response: Response, dto: UserAuthenticateDTO) -> UserDTO:
        user = await self._auth_service.authenticate(username=dto.username, password=dto.password, response=response)
        return UserDTO(id=user.id, email=user.email)

    @router.post('/logout')
    async def logout(self, response: Response, user_id=get_user_id):
        await self._auth_service.logout(user_id=user_id, response=response)
