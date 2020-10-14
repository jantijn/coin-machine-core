from use_cases.exceptions.exceptions import NonFatalWebAppException
from use_cases.handle_error import HandleError


class ListWonItems:
    def __init__(self, web_app, repository, logger):
        self.web_app = web_app
        self.repository = repository
        self.logger = logger

    def execute(self, margin, bonus):
        self.logger.log("Listing won items...")
        self._go_to_transfer_targets()
        profit = self._list_won_items(margin, bonus)
        self.logger.log(f"Listed won items! Total profit: {profit}")
        return profit

    def _go_to_transfer_targets(self):
        try:
            self.web_app.go_to_transfer_targets()
        except Exception as e:
            self._handle_error(e)
            self._go_to_transfer_targets()

    def _list_won_items(self, margin, bonus):
        profit = 0
        item_profit = margin + bonus
        while True:
            try:
                purchased_items = self.web_app.get_purchased_items()
                if len(purchased_items) == 0:
                    break
                item = purchased_items.pop(0)
                self.logger.log(f"Listing {item.name}...")
                sell_price = self._calculate_sell_price(int(item.purchase_price), margin, bonus)
                item.list(sell_price)
                # self.repository.save_purchased_item(item)
                profit += item_profit
                self.logger.log(f"Listed {item.name} at {sell_price} for a profit of {item_profit}")
            except Exception as e:
                self._handle_error(e)
        return profit

    @staticmethod
    def _calculate_sell_price(purchase_price, margin, bonus):
        ea_tax = 0.05
        return int(round(((purchase_price + margin) / (1 - ea_tax)) / 100, 0) * 100) + bonus

    def _handle_error(self, e):
        handle_error = HandleError(web_app=self.web_app, logger=self.logger)
        handle_error.execute(e)
