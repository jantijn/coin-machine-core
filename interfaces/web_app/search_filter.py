from interfaces.web_app.pages import search_the_market


class SearchFilter:
    def __init__(self, driver):
        self.driver = driver

    def fill(self, name, price):
        search_the_market.set_name(self.driver, name)
        search_the_market.set_max_bid_price(self.driver, price)

    def search(self):
        search_the_market.search_the_transfer_market(self.driver)
