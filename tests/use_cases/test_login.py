from unittest import mock

from use_cases.exceptions.exceptions import WrongCredentialsException
from use_cases.login import Login
from use_cases.responses import responses

USERNAME = "username"
PASSWORD = "password"


def test_login_happy_flow(self):
    web_app_interface = mock.Mock()
    logger_interface = mock.Mock()

    login = Login(web_app_interface, logger_interface)
    response = login.execute(username=USERNAME, password=PASSWORD)

    web_app_interface.login.assert_called_with(USERNAME, PASSWORD)
    assert bool(response) is True


def test_login_handles_wrong_username_or_password():
    web_app_interface = mock.Mock()
    web_app_interface.login.side_effect = WrongCredentialsException(
        "Wrong email address or password"
    )
    logger_interface = mock.Mock()

    login = Login(web_app_interface, logger_interface)
    response = login.execute(username=USERNAME, password=PASSWORD)

    web_app_interface.login.assert_called_with(USERNAME, PASSWORD)
    assert bool(response) is False
    assert response.value == {
        'type': responses.ResponseFailure.PARAMETERS_ERROR,
        'message': 'Wrong username and or password'
    }


def test_login_handles_generic_error():
    web_app_interface = mock.Mock()
    web_app_interface.login.side_effect = Exception(
        "Just an error message"
    )
    logger_interface = mock.Mock()

    login = Login(web_app_interface, logger_interface)
    response = login.execute(username=USERNAME, password=PASSWORD)

    assert bool(response) is False
    assert response.value == {
        'type': responses.ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: Just an error message'
    }
