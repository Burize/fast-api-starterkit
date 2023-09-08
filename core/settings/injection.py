from core.dependencies import UserId
from core.dependencies.user_id import get_user_id
from core.inject.dependency_container import DependencyContainer
from core.session import SessionStorage
from core.session.get_session_storage import get_session_storage

DependencyContainer.add(SessionStorage, get_session_storage)
DependencyContainer.add(UserId, get_user_id)
