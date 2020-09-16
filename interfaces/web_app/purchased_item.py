from entities.purchased_item import PurchasedItemInterface
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


class PurchasedItem(WebAppElement, PurchasedItemInterface):
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
        self.sell_price = sell_price
        self.slow_click()
        open_list_dialog(self.driver)
        set_start_price(self.driver, sell_price - 100)
        set_max_buy_now_price(self.driver, sell_price)
        confirm_listing(self.driver)

    def _get_purchase_price(self):
        purchase_price_string = self.get_attribute(PURCHASE_PRICE)
        if purchase_price_string:
            return int(purchase_price_string.replace(",", ""))
        return ""
