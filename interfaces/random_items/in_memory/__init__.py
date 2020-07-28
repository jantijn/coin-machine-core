import random

from interfaces.random_items.market_data import get_market_price

from entities.search_filter import SearchFilter


class SearchFilterInterface:
    def get_random_search_filters(self, number, margin=100, bonus=100):
        search_filters = []
        while len(search_filters) < number:
            search_filter = self._get_random_search_filter(margin, bonus)
            if search_filter not in search_filters:
                search_filters.append(search_filter)

    def _get_random_search_filter(self, margin, bonus):
        items = [
            {"name": "Joe Gomez", "futbin_id": "225100", "margin": 300, "bonus": 100},
            {"name": "Nathan Ake", "futbin_id": "208920", "margin": 300, "bonus": 100},
        ]
        random_item = random.choice(items)
        return self._random_item_to_search_filter(random_item, margin, bonus)

    @staticmethod
    def _random_item_to_search_filter(random_item, margin, bonus):
        search_filter = SearchFilter(random_item["name"], margin, bonus)
        search_filter.calculate_prices(get_market_price(random_item["futbin_id"]))
        return search_filter
