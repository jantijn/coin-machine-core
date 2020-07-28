import random
import time

from entities.search_filter import SearchFilter


class MassBid:
    def __init__(self, web_app, random_items, market_data, purchased_items, logger):
        self.web_app = web_app
        self.random_items = random_items
        self.market_data = market_data
        self.purchased_items = purchased_items
        self.logger = logger

    def execute(
            self,
            margin=200,
            bonus=100,
            number_of_repetitions=1,
            number_of_search_filters=1,
            max_time_left=5
    ):
        max_items = self.calculate_max_items(number_of_search_filters)

        for repetition in range(number_of_repetitions):
            self._refresh_transfer_list()
            search_filters = self._get_search_filters(number_of_search_filters, margin, bonus)
            self._bid_on_each_search_filter(max_items, max_time_left, search_filters)
            self._wait_untill_bidding_finished(max_time_left)
            won_items = self._list_won_items(search_filters)
            self._save_won_items_in_database(won_items)

    @staticmethod
    def calculate_max_items(number_of_search_filters):
        transfer_target_max_items = 50
        max_items = int(transfer_target_max_items / number_of_search_filters)
        return max_items

    def _refresh_transfer_list(self):
        self.web_app.refresh_transfer_list()

    def _get_search_filters(self, number_of_search_filters, margin, bonus):
        search_filters = []
        random_items = self.random_items.get(number_of_search_filters)
        for item in random_items:
            search_filters.append(
                self._item_to_search_filter(item, margin, bonus)
            )
        return search_filters

    def _item_to_search_filter(self, item, margin, bonus):
        search_filter = SearchFilter(item['name'], margin, bonus)
        search_filter.calculate_prices(
            self.market_data.get_market_price(item['futbin_id'])
        )
        return search_filter

    def _bid_on_each_search_filter(self, max_items, max_time_left, search_filters):
        for search_filter in search_filters:
            self.web_app.bid_on_search_filter_items(
                search_filter, max_items, max_time_left
            )

    def _wait_untill_bidding_finished(self, max_time_left):
        self._random_pause(max_time_left * 60)

    @staticmethod
    def _random_pause(time_in_seconds):
        if time_in_seconds == 0:
            return
        time.sleep(time_in_seconds + random.randint(1, 60))

    def _list_won_items(self, search_filters):
        won_items = self.web_app.list_all_transfer_targets(search_filters)
        return won_items

    def _save_won_items_in_database(self, won_items):
        for won_item in won_items:
            self.purchased_items.save_purchased_item(won_item)
