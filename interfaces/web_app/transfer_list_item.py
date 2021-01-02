from entities.purchased_item import PurchasedItemEntity
from interfaces.web_app.pages import home, transfer_list
from interfaces.web_app.pages.transfer_list import (
    NAME,
    RATING,
    POSITION,
    open_list_dialog,
    set_start_price,
    set_max_buy_now_price,
    confirm_listing,
)
from interfaces.web_app.pages.utils import WebAppElement
from use_cases.exceptions.exceptions import NonFatalWebAppException


class TransferListItems:
    def __init__(self, driver):
        self.driver = driver

    def get_all(self, type_of_item):
        transfer_list_items = transfer_list.get_available_items(self.driver, type_of_item)
        return [
            TransferListItem(web_app_element) for web_app_element in transfer_list_items
        ]


class TransferListItem(WebAppElement, PurchasedItemEntity):
    def __init__(self, web_app_element):
        super().__init__(
            driver=web_app_element.driver,
            selenium_element=web_app_element.selenium_element,
        )
        self.name = self.get_attribute(NAME)
        self.rating = self.get_attribute(RATING)
        self.position = self.get_attribute(POSITION)
        self.purchase_price = None
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
