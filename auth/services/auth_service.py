from fastapi import Depends
from passlib.context import CryptContext

from auth.models import User
from auth.repositories.user_repository import UserRepository
from core.exceptions import CustomException
from core.exceptions import NotFoundException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthenticateException(CustomException):
    pass


class AuthService:
    def __init__(self, user_repository: UserRepository = Depends()):
        self._user_repository = user_repository

    def authenticate(self, username: str, password: str) -> User:
        try:
            user = self._user_repository.get_user_by_username(username)
        except NotFoundException:
            raise AuthenticateException('username or password is invalid')

        is_password_correct = self.verify_password(password, user.password)

        if not is_password_correct:
            raise AuthenticateException('username or password is invalid')

        return user

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
