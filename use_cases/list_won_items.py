from use_cases.exceptions.exceptions import NonFatalWebAppException
from use_cases.handle_error import HandleError


class ListWonItems:
    def __init__(self, web_app, repository, logger):
        self.web_app = web_app
        self.repository = repository
        self.logger = logger

    def execute(self, margin, bonus):
        self.logger.log("Listing won items...")
        self._list_won_items(margin, bonus)

    def _list_won_items(self, margin, bonus):
        purchased_items = self.web_app.get_purchased_items()

        while len(purchased_items) > 0:
            try:
                item = purchased_items.pop(0)
                sell_price = self._calculate_sell_price(int(item.purchase_price), margin, bonus)
                item.list(sell_price)
                # self.repository.save_purchased_item(item)
                self.logger.log("Listed " + item.name)
            except NonFatalWebAppException as e:
                self._handle_error(e)
            finally:
                purchased_items = self.web_app.get_purchased_items()

    @staticmethod
    def _calculate_sell_price(purchase_price, margin, bonus):
        ea_tax = 0.05
        return int(round(((purchase_price + margin) / (1 - ea_tax)) / 100, 0) * 100) + bonus

    def _handle_error(self, e):
        handle_error = HandleError(web_app=self.web_app, logger=self.logger)
        handle_error.execute(e)
