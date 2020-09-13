import random
import time

from interfaces.web_app import utils
from interfaces.web_app.utils import WebAppObject

SEARCH_RESULTS = "li.listFUTItem.has-auction-data"
BID_PRICE_FIELD = "div.DetailPanel > div.bidOptions > div > input"
BID_BUTTON = "button.btn-standard.call-to-action.bidButton"
TIME_LEFT_LABEL = "span.time"
NAME = "div.name"
RATING = "div.rating"


class SearchResult(WebAppObject):
    def __init__(self, driver, web_app_object):
        super().__init__(driver, web_app_object)
        self.name = self.get_attribute(NAME)
        self.rating = self.get_attribute(RATING)
        self.bid_price = None
        self.time_left = self._get_time_left()

    def bid(self, price):
        try:
            self.bid_price = price

            self.slow_click()
            self.slow_click()

            bid_price_field = utils.get_element(self.driver, BID_PRICE_FIELD)
            bid_price_field.safe_fill(price)

            bid_button = utils.get_element(self.driver, BID_BUTTON)
            bid_button.slow_click()
        except:
            pass

    def to_dict(self):
        return dict(name=self.name, rating=self.rating, bid_price=self.bid_price)

    def _get_time_left(self):
        time_left_string = self.get_attribute(TIME_LEFT_LABEL)
        return self._to_number(time_left_string)

    @staticmethod
    def _to_number(time_left_string):
        number = time_left_string.split(" ")[0].replace("<", "")
        unit = time_left_string.split(" ")[1]
        if unit == "Seconds":
            return 1
        elif unit == "Hours" or unit == "Hour":
            return 60
        return int(number)


def bid_on_search_results(driver, price, max_bids, max_time_left):
    _random_pause(2)
    items_with_bid = []

    search_results = utils.get_elements(driver, SEARCH_RESULTS, class_=SearchResult)

    for search_result in search_results:
        _random_pause(1)
        if len(items_with_bid) >= max_bids or search_result.time_left >= max_time_left:
            break
        if "highest-bid" in search_result.get_classes():
            continue
        search_result.bid(price)
        items_with_bid.append(search_result.to_dict())

    return items_with_bid


def _random_pause(average_pause_time_in_seconds):
    time.sleep(average_pause_time_in_seconds + random.uniform(-0.5, 0.5))
