from dataclasses import dataclass
from uuid import UUID

from fastapi import APIRouter

from auth.models import User
from auth.repositories.user_repository import UserRepository
from core.api import controller
from core.inject import inject

router = APIRouter()



@dataclass
class UserDTO:
    username: str
    password: str
    email: str


@dataclass
class UserCreatedDTO:
    id: UUID
    username: str
    email: str


@controller
class UserController:
    @inject
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    @router.post('')
    def create(self, dto: UserDTO) -> UserCreatedDTO:
        user = User(username=dto.username, password=dto.password, email=dto.email)
        self._user_repository.save(user)

        return UserCreatedDTO(id=user.id, email=user.email, username=user.username)
