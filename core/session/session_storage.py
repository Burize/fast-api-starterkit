from dataclasses import dataclass
from abc import ABCMeta
from abc import abstractmethod
from typing import Optional
from uuid import UUID



class SessionStorage(metaclass=ABCMeta):
    @abstractmethod
    def create_session(self, user_id: UUID, session_id: str):
        pass

    @abstractmethod
    def prolong_session(self, session_id: str):
        pass

    @abstractmethod
    def get_user_active_session_id(self, user_id: UUID) -> Optional[str]:
        pass

    @abstractmethod
    def get_user_id(self, session_id: str) -> Optional[UUID]:
        pass

    @abstractmethod
    def delete_session(self, user_id: UUID):
        pass
