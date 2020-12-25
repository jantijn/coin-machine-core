from entities.search_result import SearchResultEntity
from interfaces.web_app.pages.utils import WebAppElement

NAME = "div.name"
RATING = "div.rating"
BUY_NOW_PRICE = "div.auction > div:nth-child(3) > span.currency-coins.value"


class SearchResult(WebAppElement, SearchResultEntity):
    def __init__(self, web_app_element):
        super().__init__(
            driver=web_app_element.driver,
            selenium_element=web_app_element.selenium_element,
        )
        self.name = self.get_attribute(NAME)
        self.rating = self.get_attribute(RATING)
        self.buy_now_price = self._get_buy_now_price()

    def _get_buy_now_price(self):
        purchase_price_string = self.get_attribute(BUY_NOW_PRICE)
        if purchase_price_string:
            return int(purchase_price_string.replace(",", ""))
        return 0