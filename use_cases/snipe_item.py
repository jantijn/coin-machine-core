import random
import time


def _random_pause():
    time.sleep(random.random())


class SnipeItem:
    def __init__(self, web_app, repository, market_data, logger):
        self.web_app = web_app
        self.repository = repository
        self.market_data = market_data
        self.logger = logger

    def execute(self, name, price, number_of_attempts=1):
        min_price = 0
        self.logger.log(f"Trying to snipe {name} {number_of_attempts} times...")
        self._set_search_filter(name, price)

        for attempt in range(number_of_attempts):
            success = self._snipe_item(attempt)
            if success:
                break
            min_price = self._reset_search(min_price)
            _random_pause()

        self.logger.log(f"Finished sniping {name}")

    def _set_search_filter(self, name, price):
        self.web_app.go_to_search_the_transfer_market()
        self.web_app.set_filter(name = name, price = price, strategy = 'snipe')

    def _snipe_item(self, attempt):
        self.logger.log(f"Attempt number {attempt}")
        self.web_app.search()
        [result, sniped_item] = self.web_app.snipe()
        if result == 'success':
            self.logger.log(f"Sniped {sniped_item.name} for {sniped_item.purchase_price}!")
            sniped_item.list()
            return True
        elif result == 'no_item_found':
            self.logger.log(f"No item found")
            return False
        elif result == 'outbid':
            self.logger.log(f"Outbid by other player")
            return False

    def _reset_search(self, min_price):
        self.web_app.go_back()
        min_price = min_price + 100 if min_price < 600 else 0
        self.web_app.set_min_price(min_price)
        return min_price
