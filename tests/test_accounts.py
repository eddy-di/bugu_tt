import pytest

from rest_framework.reverse import reverse

from accounts.models import User


@pytest.mark.django_db
def test_register_endpoint_with_correct_email(
    client
):
    # given: client attempts to register
    payload = {
        'email': 'test.user@example.org',
        'password': 'strongPa55'
    }
    # when: executing POST request on register endpoint
    url = reverse('register')
    response = client.post(
        url,
        data=payload,
        content_type='application/json'
    )
    print(response.content.decode('utf-8'))
    # then: expecting to get 201 code
    assert response.status_code == 201
    assert response.data['user']['email'] == payload['email']
    assert response.data['message'] == 'User registered successfully.'


@pytest.mark.django_db
def test_register_endpoint_with_incorrect_email(
    client
):
    # given: client attempts to register
    payload = {
        'email': '"><script>alert(1);</script>"@example.org',
        'password': 'strongPa55'
    }
    # when: executing POST request on register endpoint
    url = reverse('register')
    response = client.post(
        url,
        data=payload,
        content_type='application/json'
    )
    print(response.content.decode('utf-8'))
    # then: expecting to get 400 code
    assert response.status_code == 400
    assert response.data['detail'] == ['Email or password fields are incorrect.']
    assert response.data['message'] == [('Password must be at least 8 characters long, '
                                         'contain at least one uppercase and one lowercase letter.')]


@pytest.mark.django_db
def test_register_endpoint_with_incorrect_password_all_lowercase(
    client
):
    # given: client attempts to register
    payload = {
        'email': 'test.user@example.com',
        'password': 'strongpass'
    }
    # when: executing POST request on register endpoint
    url = reverse('register')
    response = client.post(
        url,
        data=payload,
        content_type='application/json'
    )
    print(response.content.decode('utf-8'))
    # then: expecting to get 400 code
    assert response.status_code == 400
    assert response.data['detail'] == ['Email or password fields are incorrect.']
    assert response.data['message'] == [('Password must be at least 8 characters long, '
                                         'contain at least one uppercase and one lowercase letter.')]


@pytest.mark.django_db
def test_register_endpoint_with_incorrect_password_all_uppercase(
    client
):
    # given: client attempts to register
    payload = {
        'email': 'test.user@example.com',
        'password': 'STRONGPASS'
    }
    # when: executing POST request on register endpoint
    url = reverse('register')
    response = client.post(
        url,
        data=payload,
        content_type='application/json'
    )
    print(response.content.decode('utf-8'))
    # then: expecting to get 400 code
    assert response.status_code == 400
    assert response.data['detail'] == ['Email or password fields are incorrect.']
    assert response.data['message'] == [('Password must be at least 8 characters long, '
                                         'contain at least one uppercase and one lowercase letter.')]


@pytest.mark.django_db
def test_register_endpoint_with_incorrect_password_bad_length(
    client
):
    # given: client attempts to register
    payload = {
        'email': 'test.user@example.com',
        'password': 'str0ngP'
    }
    # when: executing POST request on register endpoint
    url = reverse('register')
    response = client.post(
        url,
        data=payload,
        content_type='application/json'
    )
    print(response.content.decode('utf-8'))
    # then: expecting to get 400 code
    assert response.status_code == 400
    assert response.data['detail'] == ['Email or password fields are incorrect.']
    assert response.data['message'] == [('Password must be at least 8 characters long, '
                                         'contain at least one uppercase and one lowercase letter.')]


@pytest.mark.django_db
def test_register_endpoint_with_existing_email_and_password(
    client,
    create_user_with_role
):
    # given: client attepts to register with existing email
    user = create_user_with_role(role=User.SUBSCRIBER)
    payload = {
        'email': user.email,
        'password': 'strongPa55'
    }
    # when: executing POST request on register endpoint
    url = reverse('register')
    response = client.post(
        url,
        data=payload,
        content_type='application/json'
    )
    print(response.content.decode('utf-8'))
    # then: expecting to get 400 code
    assert response.status_code == 400
    assert response.data['detail'] == ['Email or password fields are incorrect.']
    assert response.data['message'] == [('Password must be at least 8 characters long, '
                                         'contain at least one uppercase and one lowercase letter.')]
    

@pytest.mark.django_db
def test_login_endpoint_with_correct_data(
    client,
    create_user_with_role
):
    # given: user that attempts to login to the server
    subscriber = create_user_with_role(role=User.SUBSCRIBER)
    payload = {
        'email': subscriber.email,
        'password': 'veryStrongP@$$123'
    }
    # when: executing login POST request
    url = reverse('login')
    response = client.post(
        url, 
        data=payload,
        content_type='application/json'
    )
    print(response.content.decode('utf-8'))
    # then: expecting success and 200 status code
    assert response.status_code == 200
    assert response.data['user']['email'] == payload['email']
    assert response.data['message'] == 'User logged in successfully.'


@pytest.mark.django_db
def test_login_endpoint_with_incorrect_data(
    client,
    create_user_with_role
):
    # given: user instance
    subscriber = create_user_with_role(role=User.SUBSCRIBER)
    payload = {
        'email': subscriber.email,
        'password': 'wrongPa55'
    }
    # when: client passes wrong payload data of user instance
    url = reverse('login')
    response = client.post(
        url,
        data=payload,
        content_type='application/json'
    )
    print(response.content.decode('utf-8'))
    # then: expexting to get error
    assert response.status_code == 400
    assert response.data['non_field_errors'] == ['Invalid login credentials']


@pytest.mark.django_db
def test_logout_enpoint(
    create_user_with_role,
    basic_api_client_pass_user
):
    # given: authenticated user
    user = create_user_with_role(role=User.SUBSCRIBER)
    client = basic_api_client_pass_user(user)
    # when: executing logout POST method
    url = reverse('logout')
    response = client.post(
        url,
        data=None,
        content_type = 'application/json'
    )
    print(response.content.decode('utf-8'))
    # then: expecting success and status code 200
    assert response.status_code == 200
    assert response.data['message'] == 'Logged out successfully.'
