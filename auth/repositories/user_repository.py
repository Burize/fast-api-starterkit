from uuid import UUID

from fastapi_sqlalchemy import db

from auth.models import User
from core.exceptions import NotFoundException


class UserRepository:
    def get(self, user_id: UUID) -> User:
        user = User.query.get(user_id)
        if not user:
            raise NotFoundException('User is not found')
        return user

    def save(self, user: User):
        db.session.add(user)
        db.session.flush()

    def get_user_by_username(self, username: str) -> User:
        user = User.query.filter(User.username.ilike(username)).one_or_none()
        if not user:
            raise NotFoundException('User is not found')
        return user
