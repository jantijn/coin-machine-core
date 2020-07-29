import unittest
from unittest import mock

from entities.search_filter import SearchFilter
from entities.purchased_item import PurchasedItem
from use_cases._list_won_items import ListWonItems

search_filter_1 = SearchFilter.from_dict({"name": "Joe Gomez", "margin": 300, "bonus": 100})
search_filter_1.calculate_prices(2000)
search_filter_2 = SearchFilter.from_dict({"name": "Nathan Ake", "margin": 300, "bonus": 100})
search_filter_2.calculate_prices(1500)

TARGET_SEARCH_FILTERS = [
    search_filter_1,
    search_filter_2,
]


class TestListWonItems(unittest.TestCase):
    def test_list_won_items(self):
        web_app = mock.Mock()
        purchased_items = mock.Mock()
        logger = mock.Mock()

        target_response = [
            PurchasedItem(search_filter_1.name, search_filter_1.buy_price, search_filter_1.sell_price),
            PurchasedItem(search_filter_2.name, search_filter_2.buy_price, search_filter_2.sell_price),
        ]

        web_app.list_all_transfer_targets.return_value = target_response

        list_won_items = ListWonItems(web_app, purchased_items, logger)
        response = list_won_items.execute(TARGET_SEARCH_FILTERS)

        web_app.list_all_transfer_targets.assert_called_with(TARGET_SEARCH_FILTERS)
        assert response == target_response


if __name__ == "__main__":
    unittest.main()
