from uuid import UUID
from fastapi import Response
from injector import inject

from core import settings
from passlib.context import CryptContext

from auth.models import User
from auth.repositories import UserRepository
from core.exceptions import CustomException
from core.exceptions import NotFoundException
from core.session import SessionStorage

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthenticateException(CustomException):
    pass


class AuthService:
    @inject
    def __init__(
        self,
        user_repository: UserRepository,
        session_storage: SessionStorage
    ):
        self._user_repository = user_repository
        self._session_storage = session_storage

    async def authenticate(self, response: Response, username: str, password: str) -> User:
        try:
            user = await self._user_repository.get_user_by_username(username)
        except NotFoundException:
            raise AuthenticateException('Username or password is invalid')

        is_password_correct = self.verify_password(password, user.password)

        if not is_password_correct:
            raise AuthenticateException('Username or password is invalid')

        session_id = pwd_context.hash(password)
        await self._session_storage.create_session(session_id=session_id, user_id=user.id)

        response.set_cookie(key=settings.USER_SESSION_NAME, max_age=settings.USER_SESSION_MAX_AGE, value=session_id)

        return user

    async def logout(self, user_id: UUID, response: Response):
        await self._session_storage.delete_session(user_id=user_id)
        response.set_cookie(key=settings.USER_SESSION_NAME, max_age=0, value='')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
