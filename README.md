# FastAPI starterkit
The REST API server starterkit based on the [FastAPI](https://fastapi.tiangolo.com/) framework. 
The starterkit implements the asynchronous programming model (async / await).

Main stack of libraries:
 - [SQLAlchemy](https://www.sqlalchemy.org/) as ORM;
 - [Redis](https://redis.io/) as session storage;
 - [Alembic](https://alembic.sqlalchemy.org/en/latest/) as migration manager;
 - [Injector](https://github.com/python-injector/injector) for dependency injection;
 - [Uvicorn](http://www.uvicorn.org/) as web server.


## Features

### Class based view
It is convenient and clear to combine all routes related to one model into a class. They use the same dependencies and work with the same model.

```python
from dataclasses import dataclass
from http import HTTPStatus
from uuid import UUID

from injector import inject

from auth.models import User
from auth.repositories import UserRepository
from core.api import APIRouter
from core.api import controller
from core.exceptions import ConflictException

router = APIRouter()


@dataclass
class CreateUserDTO:
    username: str
    password: str
    email: str


@dataclass
class UserDTO:
    id: UUID
    username: str
    email: str

    
@controller
class UserController:
    @inject
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    @router.post('', no_authetication=True, status_code=HTTPStatus.CREATED)
    async def create(self, dto: CreateUserDTO) -> UserDTO:
        user_with_same_email = await self._user_repository.find_user_by_email(dto.email)
        if user_with_same_email:
            raise ConflictException('Email is already taken')

        user_with_same_username = await self._user_repository.find_user_by_username(dto.username)
        if user_with_same_username:
            raise ConflictException('Username is already taken')

        user = User(username=dto.username, password=dto.password, email=dto.email)
        await self._user_repository.save(user)

        return UserDTO(id=user.id, email=user.email, username=user.username)
```

### Dependency injection
The dependency injection provided by FastAPI has several significant cons:
 - It creates a new thread for any class based dependency. More precisely, for any non-asynchronous function, and the `__init__` can not be async.
 - It is not possibly to get dependency without anotation (Depends or Annotated). Moreover, annotations do not work everywere. For example, middlewares are maintained by Starlette (FastAPI is based on it), so FastAPI's annotations can not be used in arguments.
 - You need to provide an annotation for each function argument. It brings a lot of boilerplate code.

Therefore, the another library ([Injector](https://github.com/python-injector/injector)) is used for dependency injection.

For example, you can easily get SessionStorage in the middleware:
```python
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint

from core import settings
from core.inject import injector
from core.session import SessionStorage


class UserSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        response = await call_next(request)

        session_id = request.cookies.get('session_id', None)
        user_id = getattr(request.state, 'user_id', None)
        is_logout = 'logout' in request.url.path
        if is_logout or not session_id or not user_id:
            return response

        session_storage = injector.get(SessionStorage)
        await session_storage.prolong_session(session_id)
        response.set_cookie(key=settings.USER_SESSION_NAME, max_age=settings.USER_SESSION_MAX_AGE, value=session_id)
        return response
```

