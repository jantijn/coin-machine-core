import unittest
from unittest import mock
from unittest.mock import call

from use_cases.mass_bid import MassBid

TARGET_NUMBER_OF_SEARCH_FILTERS = 2
TARGET_MAX_ITEMS = int(50 / TARGET_NUMBER_OF_SEARCH_FILTERS)
TARGET_MAX_TIME_LEFT = 0
TARGET_SEARCH_FILTERS = ["search_filter_1", "search_filter_2"]
TARGET_WON_ITEMS = [{"name": "player 1"}, {"name": "player 2"}]


class TestMassBid(unittest.TestCase):
    @staticmethod
    def _create_mock_mass_bid_class():
        web_app = mock.Mock()
        search_filter_repository = mock.Mock()
        item_repository = mock.Mock()
        logger = mock.Mock()

        search_filter_repository.get_random_search_filters.return_value = (
            TARGET_SEARCH_FILTERS
        )
        web_app.list_all_transfer_targets.return_value = TARGET_WON_ITEMS

        mass_bid = MassBid(web_app, search_filter_repository, item_repository, logger)
        return [mass_bid, web_app, search_filter_repository, item_repository, logger]

    def test_mass_bid_refreshes_transfer_list(self):
        [
            mass_bid,
            web_app,
            search_filter_repository,
            item_repository,
            logger,
        ] = self._create_mock_mass_bid_class()
        mass_bid.execute(max_time_left=TARGET_MAX_TIME_LEFT)

        web_app.refresh_transfer_list.assert_called_with()

    def test_mass_bid_gets_random_search_filters(self):
        [
            mass_bid,
            web_app,
            search_filter_repository,
            item_repository,
            logger,
        ] = self._create_mock_mass_bid_class()
        mass_bid.execute(
            number_of_search_filters=TARGET_NUMBER_OF_SEARCH_FILTERS,
            max_time_left=TARGET_MAX_TIME_LEFT,
        )

        search_filter_repository.get_random_search_filters.assert_called_with(
            TARGET_NUMBER_OF_SEARCH_FILTERS
        )

    def test_mass_bid_bids_on_items_for_each_search_filter(self):
        [
            mass_bid,
            web_app,
            search_filter_repository,
            item_repository,
            logger,
        ] = self._create_mock_mass_bid_class()
        mass_bid.execute(
            number_of_search_filters=TARGET_NUMBER_OF_SEARCH_FILTERS,
            max_time_left=TARGET_MAX_TIME_LEFT,
        )

        calls = [
            call(TARGET_SEARCH_FILTERS[0], TARGET_MAX_ITEMS, TARGET_MAX_TIME_LEFT),
            call(TARGET_SEARCH_FILTERS[1], TARGET_MAX_ITEMS, TARGET_MAX_TIME_LEFT),
        ]

        web_app.bid_on_search_filter_items.assert_has_calls(calls)

    def test_mass_bid_lists_all_transfer_targets(self):
        [
            mass_bid,
            web_app,
            search_filter_repository,
            item_repository,
            logger,
        ] = self._create_mock_mass_bid_class()
        mass_bid.execute(
            number_of_search_filters=TARGET_NUMBER_OF_SEARCH_FILTERS,
            max_time_left=TARGET_MAX_TIME_LEFT,
        )

        web_app.list_all_transfer_targets.assert_called_with(TARGET_SEARCH_FILTERS)

    def test_mass_bid_saves_all_won_items_in_database(self):
        [
            mass_bid,
            web_app,
            search_filter_repository,
            item_repository,
            logger,
        ] = self._create_mock_mass_bid_class()
        mass_bid.execute(
            number_of_search_filters=TARGET_NUMBER_OF_SEARCH_FILTERS,
            max_time_left=TARGET_MAX_TIME_LEFT,
        )

        calls = [call(TARGET_WON_ITEMS[0]), call(TARGET_WON_ITEMS[1])]

        item_repository.save_won_item.assert_has_calls(calls)


if __name__ == "__main__":
    unittest.main()
