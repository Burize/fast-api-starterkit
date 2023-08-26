from typing import Type

from fastapi_sqlalchemy import db
from sqlalchemy import MetaData
from sqlalchemy.orm import class_mapper
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


class QueryProperty(object):
    def __get__(self, instance, owner):
        mapper = class_mapper(owner)
        return db.session.query(mapper)


class Model:
    query = QueryProperty()


Base: Type[Model] = declarative_base(metadata=meta, cls=Model)
