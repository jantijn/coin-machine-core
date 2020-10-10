import random
import time


def _random_pause():
    time.sleep(random.random() / 10)


class SnipeItem:
    def __init__(self, web_app, repository, market_data, logger):
        self.web_app = web_app
        self.repository = repository
        self.market_data = market_data
        self.logger = logger

    def execute(self, characteristics, price, number_of_attempts=1, type_of_filter='name'):
        min_price = 150
        self.logger.log(f"Trying to snipe {characteristics['name']} {number_of_attempts} times...")

        self._set_search_filter(characteristics, price, type_of_filter)

        for attempt in range(number_of_attempts):
            success = self._snipe_item(attempt)
            if success:
                self.web_app.send_to_club()
                break
            min_price = self._reset_search(min_price)
            _random_pause()

        self.logger.log(f"Finished sniping {characteristics['name']}")

    def _set_search_filter(self, characteristics, price, type_of_filter):
        self.web_app.go_to_search_the_transfer_market()
        if type_of_filter == 'name':
            self.web_app.set_filter(name = characteristics['name'], price = price, strategy = 'snipe')
        elif type_of_filter == 'characteristics':
            self.web_app.set_filter_based_on_characteristics(
                club = characteristics['club'],
                nation = characteristics['nation'],
                position = characteristics['position'],
                price = price
            )

    def _snipe_item(self, attempt):
        self.logger.log(f"Attempt number {attempt}")
        self.web_app.search()
        [result, sniped_item] = self.web_app.snipe_item()
        if result == 'success':
            self.logger.log(f"Sniped {sniped_item['name']} for {sniped_item['purchase_price']}!")
            return True
        elif result == 'no_item_found':
            self.logger.log(f"No item found")
            return False
        elif result == 'outbid':
            self.logger.log(f"Outbid by other player")
            return False

    def _reset_search(self, min_price):
        self.web_app.go_back()
        min_price = min_price + 100 if min_price < 600 else 150
        self.web_app.set_min_bid_price(min_price)
        return min_price
