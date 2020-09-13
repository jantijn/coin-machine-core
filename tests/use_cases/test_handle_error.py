from unittest import mock

from use_cases.handle_error import HandleError


def test_handle_error():
    web_app = mock.Mock()
    logger = mock.Mock()

    uc = HandleError(web_app, logger)
    response = uc.execute()

    web_app.refresh.assert_called_with()
