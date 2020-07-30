from difflib import SequenceMatcher

from interfaces.web_app.selenium import utils
from interfaces.web_app.selenium.utils import WebAppObject

CLEAR_BUTTON = "div.ut-navigation-container-view--content > div > div > div > section:nth-child(4) > header > button"
PURCHASED_ITEMS = "li.listFUTItem.has-auction-data.won"
NAME = "div.name"
RATING = ""
PURCHASE_PRICE = "span.currency-coins.subContent"
OPEN_LIST_DIALOG_BUTTON = "div.DetailPanel > div.ut-quick-list-panel-view > div.ut-button-group > button"
START_PRICE_FIELD = "div.DetailPanel > div.ut-quick-list-panel-view > div.panelActions.open > div:nth-child(2) > div.ut-numeric-input-spinner-control > input"
MAX_BUY_NOW_FIELD = "div.DetailPanel > div.ut-quick-list-panel-view > div.panelActions.open > div:nth-child(3) > div.ut-numeric-input-spinner-control > input"
CONFIRM_LISTING_BUTTON = "div.DetailPanel > div.ut-quick-list-panel-view > div.panelActions.open > button"


class PurchasedItem(WebAppObject):
    def __init__(self, driver, web_app_object):
        super().__init__(driver, web_app_object)
        self.name = self.get_attribute(NAME)
        self.rating = self.get_attribute(RATING)
        self.purchase_price = self._get_purchase_price()
        self.sell_price = None

    def to_dict(self):
        return {
            "name": self.name,
            "rating": self.rating,
            "purchase_price": self.purchase_price,
            "sell_price": self.sell_price,
        }

    def list(self, sell_price):
        self.sell_price = sell_price
        self.web_app_object.slow_click()
        self._open_list_dialog()
        self._set_start_price(sell_price - 100)
        self._set_max_buy_now_price(sell_price)
        self._confirm_listing()

    def _open_list_dialog(self):
        open_list_dialog_button = utils.get_element(self.driver, OPEN_LIST_DIALOG_BUTTON)
        open_list_dialog_button.slow_click()

    def _set_start_price(self, price):
        start_price_field = utils.get_element(self.driver, START_PRICE_FIELD)
        start_price_field.safe_fill(price)

    def _set_max_buy_now_price(self, price):
        max_buy_now_field = utils.get_element(self.driver, MAX_BUY_NOW_FIELD)
        max_buy_now_field.safe_fill(price)

    def _confirm_listing(self):
        open_list_dialog_button = utils.get_element(self.driver, CONFIRM_LISTING_BUTTON)
        open_list_dialog_button.slow_click()

    def _get_purchase_price(self):
        purchase_price_string = self.get_attribute(PURCHASE_PRICE)
        return int(purchase_price_string.replace(",", ""))


def clear_expired_players(driver):
    clear_expired_players_button = utils.get_element(driver, CLEAR_BUTTON)
    clear_expired_players_button.slow_click()


def list_all_won_items(driver, search_filters):
    purchased_items_ = []

    purchased_items = utils.get_elements(driver, PURCHASED_ITEMS, class_=PurchasedItem)
    while len(purchased_items) > 0:
        item = purchased_items.pop(0)
        sell_price = _get_sell_price(item.name, search_filters)
        item.list(sell_price)
        purchased_items_.append(item.to_dict())

    return purchased_items_


def _get_sell_price(item_name, search_filters):
    matching_filter = _get_matching_filter(item_name, search_filters)
    return matching_filter.sell_price


def _get_matching_filter(item_name, search_filters):
    max_similar_score = 0
    matching_filter = {}
    for search_filter in search_filters:
        similar_score = SequenceMatcher(None, item_name, search_filter.name).ratio()
        if similar_score > max_similar_score:
            matching_filter = search_filter
            max_similar_score = similar_score
    return matching_filter
