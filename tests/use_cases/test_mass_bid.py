import unittest
from unittest import mock
from unittest.mock import call

from entities.search_filter import SearchFilter
from use_cases.mass_bid import MassBid


TARGET_NUMBER_OF_SEARCH_FILTERS = 2
TARGET_MAX_ITEMS = int(50 / TARGET_NUMBER_OF_SEARCH_FILTERS)
TARGET_MAX_TIME_LEFT = 0
TARGET_MARGIN = 0
TARGET_BONUS = 0
TARGET_RANDOM_ITEMS = [
    {"name": "Joe Gomez", "futbin_id": "225100", "margin": 300, "bonus": 100},
    {"name": "Nathan Ake", "futbin_id": "208920", "margin": 300, "bonus": 100},
]
TARGET_MARKET_PRICE = 2000
TARGET_WON_ITEMS = [
    {"name": "player 1"},
    {"name": "player 2"}
]


class TestMassBid(unittest.TestCase):
    @staticmethod
    def _create_mock_mass_bid_class():
        web_app = mock.Mock()
        random_items = mock.Mock()
        market_data = mock.Mock()
        purchased_items = mock.Mock()
        logger = mock.Mock()

        random_items.get.return_value = TARGET_RANDOM_ITEMS
        market_data.get_market_price.return_value = TARGET_MARKET_PRICE
        web_app.list_all_transfer_targets.return_value = TARGET_WON_ITEMS

        mass_bid = MassBid(web_app, random_items, market_data, purchased_items, logger)
        return [mass_bid, web_app, random_items, market_data, purchased_items, logger]

    def test_mass_bid_refreshes_transfer_list(self):
        [mass_bid, web_app, random_items, market_data, purchased_items, logger] = self._create_mock_mass_bid_class()
        mass_bid.execute(max_time_left=TARGET_MAX_TIME_LEFT)

        web_app.refresh_transfer_list.assert_called_with()

    def test_mass_bid_gets_random_search_filters(self):
        [mass_bid, web_app, random_items, market_data, purchased_items, logger] = self._create_mock_mass_bid_class()
        mass_bid.execute(
            number_of_search_filters=TARGET_NUMBER_OF_SEARCH_FILTERS,
            max_time_left=TARGET_MAX_TIME_LEFT,
            margin=TARGET_MARGIN,
            bonus=TARGET_BONUS,
        )

        calls = [
            call(TARGET_RANDOM_ITEMS[0]['futbin_id']),
            call(TARGET_RANDOM_ITEMS[1]['futbin_id']),
        ]

        random_items.get.assert_called_with(TARGET_NUMBER_OF_SEARCH_FILTERS)
        market_data.get_market_price.assert_has_calls(calls)

    def test_mass_bid_bids_on_items_for_each_search_filter(self):
        [mass_bid, web_app, random_items, market_data, purchased_items, logger] = self._create_mock_mass_bid_class()

        mass_bid.execute(
            number_of_search_filters=TARGET_NUMBER_OF_SEARCH_FILTERS,
            max_time_left=TARGET_MAX_TIME_LEFT,
        )

        assert web_app.bid_on_search_filter_items.call_count == TARGET_NUMBER_OF_SEARCH_FILTERS

    def test_mass_bid_lists_all_transfer_targets(self):
        [mass_bid, web_app, random_items, market_data, purchased_items, logger] = self._create_mock_mass_bid_class()
        mass_bid.execute(
            number_of_search_filters=TARGET_NUMBER_OF_SEARCH_FILTERS,
            max_time_left=TARGET_MAX_TIME_LEFT,
        )

        web_app.list_all_transfer_targets.assert_called()

    def test_mass_bid_saves_all_won_items_in_database(self):
        [mass_bid, web_app, random_items, market_data, purchased_items, logger] = self._create_mock_mass_bid_class()
        mass_bid.execute(
            number_of_search_filters=TARGET_NUMBER_OF_SEARCH_FILTERS,
            max_time_left=TARGET_MAX_TIME_LEFT,
        )

        calls = [call(TARGET_WON_ITEMS[0]), call(TARGET_WON_ITEMS[1])]

        purchased_items.save_purchased_item.assert_has_calls(calls)


if __name__ == "__main__":
    unittest.main()
