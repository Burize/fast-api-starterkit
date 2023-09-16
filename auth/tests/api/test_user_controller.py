from http import HTTPStatus

import pytest

from auth.models import User
from auth.repositories import UserRepository
from core.inject import injector


@pytest.mark.anyio
async def test_create_user(api_client):
    username = 'test'
    email = 'test@email.com'
    data = {
        'username': username,
        'password': '1234',
        'email': email,
    }

    # Act
    async with api_client:
        response = await api_client.post('api/user', json=data)

    # Assert
    assert response.status_code == HTTPStatus.CREATED
    result = response.json()

    assert result['username'] == data['username']
    assert result['email'] == data['email']

    user_repository = injector.get(UserRepository)

    created_user = await user_repository.get_user_by_username(username)
    assert created_user.email == email


@pytest.mark.anyio
async def test_create_user_error_if_email_already_taken(api_client):
    email = 'already_taken@email.com'
    user = User(username='username', password='1234', email=email)
    user_repository = injector.get(UserRepository)
    await user_repository.save(user)

    data = {
        'username': 'test',
        'password': '1234',
        'email': email,
    }

    # Act
    async with api_client:
        response = await api_client.post('api/user', json=data)

    # Assert
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'message': 'Email is already taken'}
