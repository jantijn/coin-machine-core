import random
import time

from entities.purchased_item import PurchasedItemEntity
from interfaces.web_app.pages import home, transfer_targets
from interfaces.web_app.pages.transfer_targets import (
    NAME,
    RATING,
    open_list_dialog,
    set_start_price,
    set_max_buy_now_price,
    confirm_listing,
    PURCHASE_PRICE,
)
from interfaces.web_app.pages.utils import WebAppElement
from use_cases.exceptions.exceptions import NonFatalWebAppException


class WonItems:
    def __init__(self, driver):
        self.driver = driver

    def get_all(self):
        self._random_pause(2)
        transfer_targets.clear_expired_players(self.driver)
        won_items = transfer_targets.get_won_items(self.driver)
        return [WonItem(web_app_element) for web_app_element in won_items]

    @staticmethod
    def _random_pause(average_pause_time_in_seconds):
        time.sleep(average_pause_time_in_seconds + random.uniform(-0.5, 0.5))

    def clear_lost_items(self):
        transfer_targets.clear_expired_players(self.driver)


class WonItem(WebAppElement, PurchasedItemEntity):
    def __init__(self, web_app_element):
        super().__init__(
            driver=web_app_element.driver,
            selenium_element=web_app_element.selenium_element,
        )
        self.name = self.get_attribute(NAME)
        self.rating = self.get_attribute(RATING)
        self.purchase_price = self._get_purchase_price()
        self.sell_price = None

    def list(self, sell_price):
        try:
            self.sell_price = sell_price
            self.slow_click()
            open_list_dialog(self.driver)
            set_start_price(self.driver, sell_price - 100)
            set_max_buy_now_price(self.driver, sell_price)
            confirm_listing(self.driver)
            home.wait_until_loaded(self.driver)
        except:
            raise NonFatalWebAppException

    def _get_purchase_price(self):
        purchase_price_string = self.get_attribute(PURCHASE_PRICE)
        if purchase_price_string:
            return int(purchase_price_string.replace(",", ""))
        return 0
