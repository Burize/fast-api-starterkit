from dataclasses import asdict
from dataclasses import dataclass
from uuid import UUID

from auth.services.session_storage import SessionId
from auth.services.session_storage import SessionStorage
from core.inject import inject


@dataclass
class UserSession:
    user_id: UUID


class SessionService:
    @inject
    def __init__(self, session_storage: SessionStorage):
        self._session_storage = session_storage

    async def create_session(self, user_session: UserSession) -> SessionId:
        session_id = await self._session_storage.create_session(asdict(user_session))
        return session_id

    async def get_session(self, session_id: SessionId) -> UserSession:
        user_session = await self._session_storage.get_session(session_id)
        return UserSession(user_id=user_session['user_id'])

    async def delete_session(self, session_id: SessionId):
        await self._session_storage.delete_session(session_id)

