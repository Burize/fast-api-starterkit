from dataclasses import dataclass
from uuid import UUID
from fastapi import APIRouter

from auth.services import AuthService
from auth.services.auth_service import AuthenticateException
from core.api import controller
from core.exceptions import exception_to_response
from core.inject import inject

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

    @router.post('')
    @exception_to_response(AuthenticateException, http_code=401)
    def authenticate(self, dto: UserAuthenticateDTO):
        user = self._auth_service.authenticate(username=dto.username, password=dto.password)
        return UserDTO(id=user.id, email=user.email)
