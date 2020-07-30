from unittest import mock

from use_cases.mass_bid import MassBid
from use_cases.responses import responses


def test_mass_bid_happy_flow():
    web_app = mock.Mock()
    random_items = mock.Mock()
    market_data = mock.Mock()
    purchased_items = mock.Mock()
    logger = mock.Mock()

    mass_bid = MassBid(web_app, random_items, market_data, purchased_items, logger)
    response = mass_bid.execute(max_time_left=0)

    web_app.refresh.not_called()
    assert bool(response) is True


def test_mass_refreshes_on_exception():
    web_app = mock.Mock()
    random_items = mock.Mock()
    market_data = mock.Mock()
    purchased_items = mock.Mock()
    logger = mock.Mock()

    web_app.refresh_transfer_list.side_effect = Exception("Just an error message")

    mass_bid = MassBid(web_app, random_items, market_data, purchased_items, logger)
    response = mass_bid.execute(max_time_left=0)

    assert bool(response) is True
    web_app.refresh.assert_called_with()


def test_mass_handles_generic_error_on_refresh():
    web_app = mock.Mock()
    random_items = mock.Mock()
    market_data = mock.Mock()
    purchased_items = mock.Mock()
    logger = mock.Mock()

    web_app.refresh_transfer_list.side_effect = Exception("Just an error message")

    web_app.refresh.side_effect = Exception("A second error")

    mass_bid = MassBid(web_app, random_items, market_data, purchased_items, logger)
    response = mass_bid.execute(max_time_left=0)

    assert bool(response) is False
    assert response.value == {"type": responses.ResponseFailure.SYSTEM_ERROR, "message": "Exception: A second error"}
