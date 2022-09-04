from sqlalchemy.dialects import postgresql

from core.database.base import Base
import sqlalchemy as sa


class User(Base):
    __tablename__ = 'auth.user'
    id = sa.Column(postgresql.UUID(as_uuid=True), primary_key=True)
    username = sa.Column(sa.String, nullable=False)
    password = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, nullable=False)
