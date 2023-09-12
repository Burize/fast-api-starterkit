from uuid import UUID

from sqlalchemy import select

from auth.models import User
from core.database import Session
from core.exceptions import NotFoundException


class UserRepository:
    async def get(self, user_id: UUID) -> User:
        query = select(User).filter(User.id == user_id)
        result = await Session.scalars(query)
        user = result.one_or_none()
        if not user:
            raise NotFoundException('User is not found')
        return user

    async def save(self, user: User):
        Session.add(user)
        await Session.flush()

    async def get_user_by_username(self, username: str) -> User:
        query = select(User).filter(User.username.ilike(username))
        result = await Session.scalars(query)
        user = result.one_or_none()
        if not user:
            raise NotFoundException('User is not found')
        return user
