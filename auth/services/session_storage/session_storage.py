from abc import ABCMeta
from abc import abstractmethod
from uuid import UUID

SessionId = UUID


class SessionStorage(metaclass=ABCMeta):
    @abstractmethod
    async def create_session(self, data: dict) -> SessionId:
        pass

    @abstractmethod
    async def get_session(self, session_id: SessionId) -> dict:
        pass

    @abstractmethod
    async def delete_session(self, session_id: SessionId):
        pass
