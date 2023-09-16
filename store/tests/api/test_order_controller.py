from http import HTTPStatus

import pytest

from auth.models import User
from auth.repositories import UserRepository
from core import settings
from core.inject import injector
from store.models import Order
from store.repositories import OrderRepository


@pytest.mark.anyio
async def test_create_order(api_client):
    user = User(username='username', password='1234', email='test@email.com')
    user_repository = injector.get(UserRepository)
    await user_repository.save(user)

    order_repository = injector.get(OrderRepository)
    order_1 = Order(description='Order 1', user_id=user.id)
    await order_repository.save(order_1)

    credentials = {
        'username': 'username',
        'password': '1234',
    }

    data = {'description': 'Order 2'}

    async with api_client:
        auth_response = await api_client.post('api/authenticate/login', json=credentials)
        cookies = {settings.USER_SESSION_NAME: auth_response.cookies[settings.USER_SESSION_NAME]}

        # Act
        response = await api_client.post('api/order', json=data, cookies=cookies)

    # Assert
    assert response.status_code == HTTPStatus.CREATED
    result = response.json()
    assert result['description'] == 'Order 2'
    assert result['number'] == 2

    user_orders = await user.awaitable_attrs.orders
    assert len(user_orders) == 2


@pytest.mark.anyio
async def test_get_orders(api_client):
    user_1 = User(username='username_1', password='1234', email='test_1@email.com')
    user_2 = User(username='username_2', password='1234', email='test_2@email.com')
    user_repository = injector.get(UserRepository)
    await user_repository.save(user_1)
    await user_repository.save(user_2)

    order_repository = injector.get(OrderRepository)
    orders = [Order(description=f'Order {i}', user_id=user_1.id) for i in range(1, 6)]
    for order in orders:
        await order_repository.save(order)

    order = Order(description=f'Order', user_id=user_2.id)
    await order_repository.save(order)

    credentials = {
        'username': user_1.username,
        'password': '1234',
    }

    expected_result = [
        dict(id=str(orders[0].id), number=orders[0].number, description=orders[0].description),
        dict(id=str(orders[1].id), number=orders[1].number, description=orders[1].description),
        dict(id=str(orders[2].id), number=orders[2].number, description=orders[2].description),
    ]

    async with api_client:
        auth_response = await api_client.post('api/authenticate/login', json=credentials)
        cookies = {settings.USER_SESSION_NAME: auth_response.cookies[settings.USER_SESSION_NAME]}

        # Act
        response = await api_client.get('api/order?limit=3', cookies=cookies)

    # Assert
    assert response.status_code == HTTPStatus.OK
    user_orders = response.json()
    assert user_orders == expected_result
