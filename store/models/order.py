from typing import Optional
from uuid import UUID
from uuid import uuid4

from passlib.context import CryptContext
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from auth.models.user import User
from core.database.base import Base
import sqlalchemy as sa

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Order(Base):
    __tablename__ = 'store_order'

    id = sa.Column(postgresql.UUID(as_uuid=True), primary_key=True)
    number = sa.Column(
        sa.Integer,
        sa.Sequence('store_order_number_seq'),
        nullable=False,
        unique=True,
        server_default=sa.text("nextval('store_order_number_seq'::regclass)"),
    )
    description = sa.Column(sa.Text, nullable=False)
    user_id = sa.Column(sa.ForeignKey(User.id, deferrable=True, initially='DEFERRED', ondelete='CASCADE'), nullable=False)
    user = relationship(User, foreign_keys=[user_id], backref='orders')

    def __init__(
        self,
        user_id: UUID,
        description: str,
        id_: Optional[UUID] = None
    ):
        self.user_id = user_id
        self.description = description
        self.id = id_ or uuid4()
