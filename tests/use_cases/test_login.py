import unittest
from unittest import mock

from interfaces.web_app.selenium.exceptions import WrongCredentialsError
from use_cases.login import Login

USERNAME = 'username'
PASSWORD = 'password'


class TestLogin(unittest.TestCase):
    def test_login_happy_flow(self):
        web_app_interface = mock.Mock()
        logger_interface = mock.Mock()

        target_response = {
            'success': True,
            'message': 'Login successful!'
        }

        login = Login(web_app_interface, logger_interface)
        response = login.execute(username = USERNAME, password = PASSWORD)

        web_app_interface.login.assert_called_with(USERNAME, PASSWORD)
        assert response == target_response

    def test_login_wrong_username_or_password(self):
        web_app_interface = mock.Mock()
        web_app_interface.login.side_effect = WrongCredentialsError("Wrong email address or password")
        logger_interface = mock.Mock()

        target_response = {
            'success': False,
            'message': 'Wrong username and or password'
        }

        login = Login(web_app_interface, logger_interface)
        response = login.execute(username = USERNAME, password = PASSWORD)

        web_app_interface.login.assert_called_with(USERNAME, PASSWORD)
        assert response == target_response


if __name__ == '__main__':
    unittest.main()
