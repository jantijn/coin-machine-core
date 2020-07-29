import unittest
from unittest import mock

from use_cases._refresh_transfer_list import RefreshTransferList


class TestRefreshTransferList(unittest.TestCase):
    def test_refresh_transfer_list(self):
        web_app = mock.Mock()
        logger = mock.Mock()

        refresh_transfer_list = RefreshTransferList(web_app, logger)
        response = refresh_transfer_list.execute()

        web_app.refresh_transfer_list.assert_called_with()


if __name__ == "__main__":
    unittest.main()
