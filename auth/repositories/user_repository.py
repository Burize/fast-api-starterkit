from fastapi import Depends
from fastapi_sqlalchemy import db

from auth.models import User
from core.exceptions import NotFoundException


class UserRepository:
    def save(self, user: User):
        db.session.add(user)
        db.session.flush()

    def get_user_by_username(self, username: str) -> User:
        user = User.query.filter(User.username.ilike(username)).one_or_none()
        if not user:
            raise NotFoundException('User is not found')
        return user