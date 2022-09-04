from fastapi import Depends
from fastapi_sqlalchemy import db
from sqlalchemy.orm import Session

from auth.models import User


class UserRepository:
    def get_user_by_username(self, username: str):
        user = db.session.query(User).first()
        return user
