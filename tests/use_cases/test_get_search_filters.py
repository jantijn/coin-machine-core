import unittest
from unittest import mock

from entities.search_filter import SearchFilter
from use_cases.get_search_filters import GetSearchFilters

TARGET_MARGIN = 300
TARGET_BONUS = 100
TARGET_MARKET_PRICE = 2000
TARGET_ITEMS = [
    {"name": "Joe Gomez", "margin": TARGET_MARGIN, "bonus": TARGET_BONUS, "futbin_id": 12345},
    {"name": "Nathan Ake", "margin": TARGET_MARGIN, "bonus": TARGET_BONUS, "futbin_id": 67890},
]

search_filter_1 = SearchFilter.from_dict(TARGET_ITEMS[0])
search_filter_1.calculate_prices(TARGET_MARKET_PRICE)
search_filter_2 = SearchFilter.from_dict(TARGET_ITEMS[1])
search_filter_2.calculate_prices(TARGET_MARKET_PRICE)

TARGET_SEARCH_FILTERS = [
    search_filter_1,
    search_filter_2,
]

TARGET_MAX_ITEMS = int(50 / len(TARGET_SEARCH_FILTERS))
TARGET_MAX_TIME_LEFT = 0


class TestGetSearchFilters(unittest.TestCase):
    def test_get_search_filters(self):
        random_items = mock.Mock()
        market_data = mock.Mock()
        logger = mock.Mock()

        random_items.get.return_value = TARGET_ITEMS
        market_data.get_market_price.return_value = 2000

        get_search_filters = GetSearchFilters(random_items, market_data, logger)
        response = get_search_filters.execute(
            margin = TARGET_MARGIN,
            bonus = TARGET_BONUS,
            number_of_search_filters = len(TARGET_ITEMS)
        )

        assert response[0].to_dict() == TARGET_SEARCH_FILTERS[0].to_dict()
        assert response[1].to_dict() == TARGET_SEARCH_FILTERS[1].to_dict()


if __name__ == "__main__":
    unittest.main()
