from difflib import SequenceMatcher

from use_cases.handle_error import HandleError
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementNotInteractableException,
)


class ListWonItems:
    def __init__(self, web_app, repository, logger):
        self.web_app = web_app
        self.repository = repository
        self.logger = logger

    def execute(self, search_filters):
        self.logger.log("Listing won items...")
        self._list_won_items(search_filters)

    def _list_won_items(self, search_filters):
        purchased_items = self.web_app.get_purchased_items()

        while len(purchased_items) > 0:
            try:
                item = purchased_items.pop(0)

                sell_price = self._get_sell_price(item, search_filters)
                item.list(sell_price)
                self.repository.save_purchased_item(item)
            except (StaleElementReferenceException, ElementNotInteractableException):
                pass
            finally:
                purchased_items = self.web_app.get_purchased_items()

    def _get_sell_price(self, item, search_filters):
        search_filter = self._get_matching_filter(item.name, search_filters)
        return search_filter.sell_price

    def _handle_error(self, e):
        handle_error = HandleError(web_app=self.web_app, logger=self.logger)
        handle_error.execute(e)

    @staticmethod
    def _get_matching_filter(item_name, search_filters):
        max_similar_score = 0
        matching_filter = {}
        for search_filter in search_filters:
            similar_score = SequenceMatcher(None, item_name, search_filter.name).ratio()
            if similar_score > max_similar_score:
                matching_filter = search_filter
                max_similar_score = similar_score
        return matching_filter
