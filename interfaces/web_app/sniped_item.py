from entities.purchased_item import PurchasedItemEntity
from interfaces.web_app.pages import home
from interfaces.web_app.pages.search_results import open_list_dialog, set_start_price, set_max_buy_now_price, \
    confirm_listing, SNIPED_ITEM_NAME, SNIPED_ITEM_RATING, SNIPED_ITEM_PURCHASE_PRICE, send_to_club, \
    send_to_transfer_list
from interfaces.web_app.pages.utils import WebAppElement


class SnipedItem(WebAppElement, PurchasedItemEntity):
    def __init__(self, web_app_element):
        super().__init__(
            driver=web_app_element.driver,
            selenium_element=web_app_element.selenium_element,
        )
        self.name = self.get_attribute(SNIPED_ITEM_NAME)
        self.rating = self.get_attribute(SNIPED_ITEM_RATING)
        self.purchase_price = self._get_purchase_price()
        self.sell_price = None

    def list(self, sell_price):
        self.sell_price = sell_price
        self.calculate_profit()
        open_list_dialog(self.driver)
        set_start_price(self.driver, sell_price - 100)
        set_max_buy_now_price(self.driver, sell_price)
        confirm_listing(self.driver)
        home.wait_until_loaded(self.driver)

    def send_to_club(self):
        send_to_club(self.driver)

    def send_to_transfer_list(self):
        send_to_transfer_list(self.driver)

    def _get_purchase_price(self):
        purchase_price_string = self.get_attribute(SNIPED_ITEM_PURCHASE_PRICE)
        if purchase_price_string:
            return int(purchase_price_string.replace(",", ""))
        return 0
