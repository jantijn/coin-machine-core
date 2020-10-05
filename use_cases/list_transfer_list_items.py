from use_cases.exceptions.exceptions import NonFatalWebAppException
from use_cases.handle_error import HandleError


class ListTransferListItems:
    def __init__(self, web_app, repository, market_data, logger):
        self.web_app = web_app
        self.repository = repository
        self.market_data = market_data
        self.logger = logger

    def execute(self):
        self.logger.log("Listing transfer list items...")
        self._list_transfer_list_items()

    def _list_transfer_list_items(self):
        transfer_list_items = self.web_app.get_transfer_list_items()

        while len(transfer_list_items) > 0:
            try:
                item = transfer_list_items.pop(0)
                sell_price = self._calculate_sell_price(item)
                item.list(sell_price)
                self.logger.log(f"Listed {item.name}, {item.position}, {item.rating} for {sell_price}")
            except NonFatalWebAppException as e:
                self._handle_error(e)
            finally:
                transfer_list_items = self.web_app.get_transfer_list_items()

    def _handle_error(self, e):
        handle_error = HandleError(web_app=self.web_app, logger=self.logger)
        handle_error.execute(e)

    def _calculate_sell_price(self, item, platform="ps"):
        item_info = self.repository.get_item_info(name=item.name, rating=item.rating, position=item.position)
        return item_info["last_market_price"]
