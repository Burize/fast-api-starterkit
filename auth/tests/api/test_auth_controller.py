from http import HTTPStatus

import pytest

from auth.models import User
from auth.repositories import UserRepository
from core import settings
from core.inject import injector


@pytest.mark.anyio
async def test_login(api_client):
    user = User(username='username', password='1234', email='test@email.com')
    user_repository = injector.get(UserRepository)
    await user_repository.save(user)

    data = {
        'username': user.username,
        'password': '1234',
    }

    # Act
    async with api_client:
        response = await api_client.post('api/authenticate/login', json=data)

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'email': user.email, 'id': str(user.id)}
    assert response.cookies.get(settings.USER_SESSION_NAME, None)


@pytest.mark.anyio
async def test_login_wrong_credentials(api_client):
    user = User(username='username', password='1234', email='test@email.com')
    user_repository = injector.get(UserRepository)
    await user_repository.save(user)

    data = {
        'username': user.username,
        'password': 'wrong',
    }

    # Act
    async with api_client:
        response = await api_client.post('api/authenticate/login', json=data)

    # Assert
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Username or password is invalid'}
    assert response.cookies.get(settings.USER_SESSION_NAME, None) is None
