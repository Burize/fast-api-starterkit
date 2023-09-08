from dataclasses import dataclass
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from auth.models import User
from auth.repositories.user_repository import UserRepository
from core.api import controller
from core.dependencies import UserId
from core.dependencies.authoroized import authorized
from core.inject import inject

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
    def __init__(self, user_repository: UserRepository,  user_id: UserId):
        self._user_repository = user_repository
        self._user_id = user_id

    @router.post('')
    def create(self, dto: CreateUserDTO) -> UserDTO:
        user = User(username=dto.username, password=dto.password, email=dto.email)
        self._user_repository.save(user)

        return UserDTO(id=user.id, email=user.email, username=user.username)

    @router.get('/my', dependencies=[Depends(authorized)])
    def get(self) -> UserDTO:
        user = self._user_repository.get(self._user_id)
        return UserDTO(id=user.id, email=user.email, username=user.username)
