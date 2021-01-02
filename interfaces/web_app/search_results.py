import random
import time

from entities.search_result import SearchResultEntity
from interfaces.web_app.pages import search_results
from interfaces.web_app.pages.search_results import TIME_LEFT_LABEL, NAME, RATING
from interfaces.web_app.pages.utils import WebAppElement


class SearchResults:
    def __init__(self, driver):
        self.driver = driver

    def get_all(self):
        self._random_pause(2)
        search_result_items = search_results.get_search_results(self.driver)
        return [
            SearchResult(web_app_element) for web_app_element in search_result_items
        ]

    @staticmethod
    def _random_pause(average_pause_time_in_seconds):
        time.sleep(average_pause_time_in_seconds + random.uniform(-0.5, 0.5))


class SearchResult(WebAppElement, SearchResultEntity):
    def __init__(self, web_app_element):
        super().__init__(
            driver=web_app_element.driver,
            selenium_element=web_app_element.selenium_element,
        )
        self.name = self.get_attribute(NAME)
        self.rating = self.get_attribute(RATING)
        self.time_left = self._get_time_left()
        self.bid_price = None

    def _get_time_left(self):
        time_left_string = self.get_attribute(TIME_LEFT_LABEL)
        return self._convert_time_string_to_number(time_left_string)

    @staticmethod
    def _convert_time_string_to_number(time_left_string):
        try:
            number = time_left_string.split(" ")[0].replace("<", "")
            unit = time_left_string.split(" ")[1]
        except:
            return 60
        if unit == "Seconds":
            return 1
        elif unit == "Hours" or unit == "Hour":
            return 60
        return int(number)

    def bid(self, price):
        try:
            self._select()
            self._set_bid_price(price)
            self._place_bid()
        except:
            pass

    def _select(self):
        self.slow_click()
        self.slow_click()

    def _set_bid_price(self, price):
        search_results.set_bid_price(self.driver, price)

    def _place_bid(self):
        search_results.place_bid(self.driver)
