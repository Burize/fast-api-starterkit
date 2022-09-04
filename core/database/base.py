from typing import Type

from fastapi_sqlalchemy import db
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.orm import Query
from sqlalchemy.orm import declarative_base

meta = MetaData(
    naming_convention={
        'ix': 'ix_%(column_0_label)s',
        'uq': 'uq_%(table_name)s_%(column_0_name)s',
        'ck': 'ck_%(table_name)s_%(constraint_name)s',
        'fk': 'fk_%(table_name)s_%(column_0_name)s',
        'pk': 'pk_%(table_name)s',
    }
)


class Model:
    @staticmethod
    def query() -> Query:
        return db.session.query_property(query_cls=Query)


Base: Type[Model] = declarative_base(metadata=meta, cls=Model)
