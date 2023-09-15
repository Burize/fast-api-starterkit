from dataclasses import dataclass
from http import HTTPStatus
from uuid import UUID

from injector import inject

from auth.models import User
from auth.repositories.user_repository import UserRepository
from core.api import APIRouter
from core.api import controller
from core.dependencies import get_user_id

router = APIRouter()


@dataclass
class CreateUserDTO:
    username: str
    password: str
    email: str


@dataclass
class UserDTO:
    id: UUID
    username: str
    email: str


@controller
class UserController:
    @inject
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    @router.post('', no_authetication=True, status_code=HTTPStatus.CREATED)
    async def create(self, dto: CreateUserDTO) -> UserDTO:
        user = User(username=dto.username, password=dto.password, email=dto.email)
        await self._user_repository.save(user)

        return UserDTO(id=user.id, email=user.email, username=user.username)

    @router.get('/my')
    async def get(self, user_id=get_user_id) -> UserDTO:
        user = await self._user_repository.get(user_id)
        return UserDTO(id=user.id, email=user.email, username=user.username)
