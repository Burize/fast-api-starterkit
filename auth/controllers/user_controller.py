from dataclasses import dataclass
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from auth.models import User
from auth.repositories.user_repository import UserRepository

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


@router.post('')
def create_user(dto: UserDTO, user_repository: UserRepository = Depends()) -> UserCreatedDTO:
    user = User(username=dto.username, password=dto.password, email=dto.email)
    user_repository.save(user)

    return UserCreatedDTO(id=user.id, email=user.email, username=user.username)
