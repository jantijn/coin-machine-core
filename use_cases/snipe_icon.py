import random
import time

from use_cases.handle_error import HandleError


def _random_pause():
    time.sleep(random.random() / 10)


class SnipeIcon:
    def __init__(self, web_app, repository, market_data, logger):
        self.web_app = web_app
        self.repository = repository
        self.market_data = market_data
        self.logger = logger

    def execute(self, number_of_attempts):
        action = 'increment'
        price_list = []
        total_profit = 0

        for attempt in range(number_of_attempts):
            print("Attempting to snipe icon...")
            print(f"Attempt number: {attempt}")
            self.web_app.search()
            time.sleep(1 + random.uniform(-0.5, 0.5))
            search_results = self.web_app.get_search_results()
            for search_result in search_results:
                try:
                    [market_price, price_list] = self._calculate_sell_price(search_result, price_list)
                except:
                    print(search_result.name)
                profit = market_price * 0.95 - search_result.buy_now_price
                if profit > 0:
                    print(f"Name: {search_result.name}")
                    print(f"Rating: {search_result.rating}")
                    print(f"Buy now price: {search_result.buy_now_price}")
                    print(f"Market price: {market_price}")
                    print(f"Profit: {profit}")
                    print()
                    total_profit += profit
            action = self._reset_search(action)

        print("Finished sniping!")
        print(f"Total profit: {total_profit}")

    def _calculate_sell_price(self, item, price_list, platform="ps"):
        market_price = self._get_market_price_from_list(price_list, item.name + item.rating)
        if market_price:
            return [market_price, price_list]

        item_info = self.repository.get_item_info(name=item.name, rating=item.rating)
        market_price = item_info["last_market_price"]
        price_list.append({"key": item.name + item.rating, "price": market_price})
        return [market_price, price_list]

    def _get_market_price_from_list(self, price_list, key):
        for item in price_list:
            if item['key'] == key:
                return item["price"]
        else:
            return False

    def _reset_search(self, action):
        self.web_app.go_back()
        time.sleep(10 + random.uniform(-0.5, 0.5))
        if action == 'increment':
            self.web_app.increment_min_bid_price()
            self.web_app.increment_min_bid_price()
            return 'decrement'
        elif action == 'decrement':
            self.web_app.decrement_min_bid_price()
            self.web_app.decrement_min_bid_price()
            return 'increment'
