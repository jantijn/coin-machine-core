from unittest import mock

from use_cases.bid_on_items import BidOnItems


mock_fut_web_app_service = mock.Mock()
mock_fut_web_app_service.bid_service.get_search_results.return_value = [1]
mock_fut_web_app_service.bid_service.get_time_left.return_value = 4
mock_logging_service = mock.Mock()

PRICE = 1000


def test_bid_on_items():
    bid_on_items = BidOnItems(
        fut_web_app_service = mock_fut_web_app_service,
        logging_service = mock_logging_service
    )
    result = bid_on_items.execute(PRICE)

    assert result is True
