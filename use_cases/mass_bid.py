import random
import time


class MassBid:
    def __init__(self, web_app, search_filter_repository, item_repository, logger):
        self.web_app = web_app
        self.search_filter_repository = search_filter_repository
        self.item_repository = item_repository
        self.logger = logger

    def execute(self, number_of_repetitions=1, number_of_search_filters=1, max_time_left=5):
        max_items = int(50 / number_of_search_filters)
        time_to_pause_in_seconds = max_time_left * 60
        for repetition in range(number_of_repetitions):
            self.web_app.refresh_transfer_list()
            search_filters = self.search_filter_repository.get_random_search_filters(number_of_search_filters)
            for search_filter in search_filters:
                self.web_app.bid_on_search_filter_items(search_filter, max_items, max_time_left)
            self._random_pause(time_to_pause_in_seconds)
            won_items = self.web_app.list_all_transfer_targets(search_filters)
            for won_item in won_items:
                self.item_repository.save_won_item(won_item)

    @staticmethod
    def _random_pause(time_in_seconds):
        if time_in_seconds == 0:
            return
        time.sleep(time_in_seconds + random.randint(1, 60))
