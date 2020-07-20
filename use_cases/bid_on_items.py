import time
import random


def random_pause(seconds):
    time.sleep(seconds + random.uniform(-0.5, 0.5))


class BidOnItems:
    def __init__(
        self,
        search_service,
        bid_service,
        navigation_service,
        logging_service,
    ):
        self._search_service = search_service
        self._bid_service = bid_service
        self._navigation_service = navigation_service
        self._logging_service = logging_service

    def execute(self, price, max_items = 20, max_time_left = 60):
        self.search_market()
        random_pause(1.5)
        self.bid_on_items(price, max_items, max_time_left)
        random_pause(1.5)
        self.go_back_to_search()

    def search_market(self):
        self._logging_service.log("Searching the transfer market")
        self._search_service.search()

    def bid_on_items(self, price, max_items, max_time_left):
        number_of_items_bid_on = 0

        for item in self._bid_service.get_search_results():
            random_pause(1)
            if number_of_items_bid_on >= max_items:
                break
            if self._bid_service.get_time_left(item) >= max_time_left:
                break
            self.bid_on_item(item, price)
            number_of_items_bid_on = number_of_items_bid_on + 1

    def bid_on_item(self, item, price):
        self._bid_service.select(item)
        self._bid_service.set_bid_price(price)
        self._bid_service.bid()
        print('Placed bid on item')

    def go_back_to_search(self):
        while self._navigation_service.get_location() != "SEARCH THE TRANSFER MARKET":
            self._navigation_service.go_back()
        print('Going back to search')
