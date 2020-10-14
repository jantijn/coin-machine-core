import random
import time

from use_cases.handle_error import HandleError


def _random_pause():
    time.sleep(random.random() / 10)


class SnipeItem:
    def __init__(self, web_app, repository, market_data, logger):
        self.web_app = web_app
        self.repository = repository
        self.market_data = market_data
        self.logger = logger

    def execute(self, characteristics, price, number_of_attempts=1, type_of_filter='name'):
        self.logger.log(f"Trying to snipe {characteristics['name']} {number_of_attempts} times...")
        self._set_search_filter(characteristics, price, type_of_filter)
        self._snipe_items(characteristics, number_of_attempts, price, type_of_filter)
        self.logger.log(f"Finished sniping {characteristics['name']}")

    def _snipe_items(self, characteristics, number_of_attempts, price, type_of_filter):
        action = 'increment'
        for attempt in range(number_of_attempts):
            try:
                success = self._snipe_item(attempt)
                if success:
                    self.web_app.send_to_club()
                    break
                action = self._reset_search(action)
                _random_pause()
            except Exception as e:
                self._handle_error(e)
                self._set_search_filter(characteristics, price, type_of_filter)

    def _set_search_filter(self, characteristics, price, type_of_filter):
        try:
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
        except Exception as e:
            self._handle_error(e)
            self._set_search_filter(characteristics, price, type_of_filter)

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

    def _reset_search(self, action):
        self.web_app.go_back()
        if action == 'increment':
            self.web_app.increment_min_bid_price()
            self.web_app.increment_min_bid_price()
            return 'decrement'
        elif action == 'decrement':
            self.web_app.decrement_min_bid_price()
            self.web_app.decrement_min_bid_price()
            return 'increment'

    def _handle_error(self, e):
        handle_error = HandleError(web_app=self.web_app, logger=self.logger)
        handle_error.execute(e)
