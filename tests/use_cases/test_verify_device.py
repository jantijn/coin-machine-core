from unittest import mock

from use_cases.exceptions.exceptions import WrongVerificationCodeError
from use_cases.responses import responses
from use_cases.verify_device import VerifyDevice

VERIFICATION_CODE = "123456789"


def test_verify_device_happy_flow():
    web_app_interface = mock.Mock()
    logger_interface = mock.Mock()

    verify_device = VerifyDevice(web_app_interface, logger_interface)
    response = verify_device.execute(verification_code=VERIFICATION_CODE)

    web_app_interface.verify_device.assert_called_with(VERIFICATION_CODE)
    assert bool(response) is True


def test_login_wrong_username_or_password():
    web_app_interface = mock.Mock()
    web_app_interface.verify_device.side_effect = WrongVerificationCodeError(
        "Wrong verification code"
    )
    logger_interface = mock.Mock()

    verify_device = VerifyDevice(web_app_interface, logger_interface)
    response = verify_device.execute(verification_code=VERIFICATION_CODE)

    web_app_interface.verify_device.assert_called_with(VERIFICATION_CODE)
    assert response.value == {
        "type": responses.ResponseFailure.PARAMETERS_ERROR,
        "message": "Wrong verification code",
    }


def test_verify_device_handles_generic_error():
    web_app_interface = mock.Mock()
    web_app_interface.verify_device.side_effect = Exception("Just an error message")
    logger_interface = mock.Mock()

    verify_device = VerifyDevice(web_app_interface, logger_interface)
    response = verify_device.execute(verification_code=VERIFICATION_CODE)

    assert bool(response) is False
    assert response.value == {
        "type": responses.ResponseFailure.SYSTEM_ERROR,
        "message": "Exception: Just an error message",
    }
