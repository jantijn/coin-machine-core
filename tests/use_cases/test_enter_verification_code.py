import unittest
from unittest import mock

from use_cases.enter_verification_code import EnterVerificationCode

CODE = 1234


class TestEnterVerificationCode(unittest.TestCase):
    def test_enter_verification_code(self):
        mock_fut_web_app_service = mock.Mock()
        mock_fut_web_app_service.login_service.wrong_verification_code.return_value = False
        mock_logging_service = mock.Mock()

        enter_verification_code = EnterVerificationCode(
            fut_web_app_service = mock_fut_web_app_service,
            logging_service = mock_logging_service
        )
        result = enter_verification_code.execute(CODE)

        assert result is True

    def test_enter_verification_code_wrong_code(self):
        mock_fut_web_app_service = mock.Mock()
        mock_fut_web_app_service.login_service.wrong_verification_code.return_value = True
        mock_logging_service = mock.Mock()

        enter_verification_code = EnterVerificationCode(
            fut_web_app_service = mock_fut_web_app_service,
            logging_service = mock_logging_service
        )
        result = enter_verification_code.execute(CODE)

        assert result is False
