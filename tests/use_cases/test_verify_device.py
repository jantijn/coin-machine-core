import unittest
from unittest import mock

from interfaces.web_app.selenium.exceptions import WrongVerificationCodeError
from use_cases.verify_device import VerifyDevice

VERIFICATION_CODE = '123456789'


class TestVerifyDevice(unittest.TestCase):
    def test_verify_device_happy_flow(self):
        web_app_interface = mock.Mock()
        logger_interface = mock.Mock()

        target_response = {
            'success': True,
            'message': 'Verify device successful'
        }

        verify_device = VerifyDevice(web_app_interface, logger_interface)
        response = verify_device.execute(verification_code = VERIFICATION_CODE)

        web_app_interface.verify_device.assert_called_with(VERIFICATION_CODE)
        assert response == target_response

    def test_login_wrong_username_or_password(self):
        web_app_interface = mock.Mock()
        web_app_interface.verify_device.side_effect = WrongVerificationCodeError("Wrong verification code")
        logger_interface = mock.Mock()

        target_response = {
            'success': False,
            'message': 'Wrong verification code'
        }

        verify_device = VerifyDevice(web_app_interface, logger_interface)
        response = verify_device.execute(verification_code = VERIFICATION_CODE)

        web_app_interface.verify_device.assert_called_with(VERIFICATION_CODE)
        assert response == target_response


if __name__ == '__main__':
    unittest.main()
