import unittest
from unittest import mock
from unittest.mock import call

from entities.search_filter import SearchFilter
from use_cases._bid_on_each_search_filter import BidOnEachSearchFilter

search_filter_1 = SearchFilter.from_dict({"name": "Joe Gomez", "margin": 300, "bonus": 100})
search_filter_1.calculate_prices(2000)
search_filter_2 = SearchFilter.from_dict({"name": "Nathan Ake", "margin": 300, "bonus": 100})
search_filter_2.calculate_prices(1500)

TARGET_SEARCH_FILTERS = [
    search_filter_1,
    search_filter_2,
]

TARGET_MAX_ITEMS = int(50 / len(TARGET_SEARCH_FILTERS))
TARGET_MAX_TIME_LEFT = 0


class TestBidOnEachFilter(unittest.TestCase):
    def test_mass_bid_bids_on_items_for_each_search_filter(self):
        web_app = mock.Mock()
        logger = mock.Mock()

        bid_on_each_search_filter = BidOnEachSearchFilter(web_app, logger)
        response = bid_on_each_search_filter.execute(
            search_filters=TARGET_SEARCH_FILTERS, max_time_left=TARGET_MAX_TIME_LEFT
        )

        calls = [
            call(TARGET_SEARCH_FILTERS[0], TARGET_MAX_ITEMS, TARGET_MAX_TIME_LEFT),
            call(TARGET_SEARCH_FILTERS[1], TARGET_MAX_ITEMS, TARGET_MAX_TIME_LEFT),
        ]

        web_app.bid_on_search_filter_items.assert_has_calls(calls)


if __name__ == "__main__":
    unittest.main()
