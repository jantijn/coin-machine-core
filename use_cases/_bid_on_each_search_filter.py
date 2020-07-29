import random
import time


class BidOnEachSearchFilter:
    def __init__(self, web_app, logger):
        self.web_app = web_app
        self.logger = logger

    def execute(self, search_filters, max_time_left=5):
        max_items = self.calculate_max_items(search_filters)
        for search_filter in search_filters:
            self.logger.log(f"Bidding on {search_filter.name}")
            self.web_app.bid_on_search_filter_items(
                search_filter, max_items, max_time_left
            )
        self._wait_until_bidding_finished(max_time_left)

    @staticmethod
    def calculate_max_items(search_filters):
        transfer_target_max_items = 50
        max_items = int(transfer_target_max_items / len(search_filters))
        return max_items

    def _wait_until_bidding_finished(self, max_time_left):
        if max_time_left == 0:
            return
        self.logger.log("Waiting until auctions with bid are finished...")
        pause_in_seconds = max_time_left * 60 + random.randint(1, 60)
        for seconds_left in reversed(range(pause_in_seconds)):
            self.logger.log(f"Seconds left: {seconds_left}")
            time.sleep(1)
