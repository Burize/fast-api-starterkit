from fastapi import Depends

from auth.models import User
from auth.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository = Depends()):
        self._user_repository = user_repository

    def authenticate(self) -> User:
        return self._user_repository.get_user_by_username('asd')
