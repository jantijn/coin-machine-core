import time
import random


def random_pause(seconds):
    time.sleep(seconds + random.uniform(-0.5, 0.5))


class BidOnItems:
    def __init__(self, fut_web_app_service, logging_service):
        self.fut_web_app_service = fut_web_app_service
        self.logging_service = logging_service

    def execute(self, price, max_items=20, max_time_left=60):
        self.search_market()
        random_pause(1)
        self.bid_on_items(price, max_items, max_time_left)
        random_pause(1)
        self.go_back_to_search()

    def search_market(self):
        self.logging_service.log("Searching the transfer market")
        self.fut_web_app_service.search_service.search()

    def bid_on_items(self, price, max_items, max_time_left):
        self.logging_service.log("Bidding on items")
        number_of_items_bid_on = 0

        for item in self.fut_web_app_service.bid_service.get_search_results():
            random_pause(1)
            if number_of_items_bid_on >= max_items:
                break
            if self.fut_web_app_service.bid_service.get_time_left(item) >= max_time_left:
                break
            self.bid_on_item(item, price)
            number_of_items_bid_on = number_of_items_bid_on + 1

    def bid_on_item(self, item, price):
        self.fut_web_app_service.bid_service.select(item)
        self.fut_web_app_service.bid_service.set_bid_price(price)
        self.fut_web_app_service.bid_service.bid()
        self.logging_service.log('Placed bid on item')

    def go_back_to_search(self):
        while self.fut_web_app_service.navigation_service.get_location() != "SEARCH THE TRANSFER MARKET":
            self.fut_web_app_service.navigation_service.go_back()
        self.logging_service.log('Going back to search')
