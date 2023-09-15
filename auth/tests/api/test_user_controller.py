from http import HTTPStatus


def test_create_user(api_client):

    data = {
        'username': 'test',
        'password': '1234',
        'email': 'test@email.com',
    }

    response = api_client.post('api/user', json=data)

    assert response.status_code == HTTPStatus.CREATED
    result = response.json()

    assert result['username'] == data['username']
    assert result['email'] == data['email']


def test_create_user_error_if_email_already_taken(api_client):
    data = {
        'username': 'test',
        'password': '1234',
        'email': 'test@email.com',
    }

    response = api_client.post('api/user', json=data)

    assert response.status_code == HTTPStatus.CREATED
    result = response.json()

    assert result['username'] == data['username']
    assert result['email'] == data['email']
