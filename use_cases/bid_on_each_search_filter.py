from use_cases.handle_error import HandleError


class BidOnEachSearchFilter:
    def __init__(self, web_app, logger):
        self.web_app = web_app
        self.logger = logger

    def execute(self, search_filters, max_time_left=5):
        max_items = self.calculate_max_items(search_filters)
        items_with_bid = 0
        for search_filter in search_filters:
            try:
                items_with_bid += self._bid_on_search_filter(max_items, max_time_left, search_filter)
            except Exception as e:
                self._handle_error(e)
        return items_with_bid

    def _bid_on_search_filter(self, max_items, max_time_left, search_filter):
        self.logger.log(f"Bidding on {search_filter.name}...")
        self.web_app.go_to_search_the_transfer_market()
        self.web_app.set_filter(
            name = search_filter.name, price = search_filter.buy_price, strategy = 'bid'
        )
        self.web_app.search()
        items = self.web_app.bid_on_search_filter_items(search_filter, max_items, max_time_left)
        self.logger.log(f"Finished bidding on {search_filter.name}")
        return items

    def _handle_error(self, e):
        handle_error = HandleError(web_app=self.web_app, logger=self.logger)
        handle_error.execute(e)

    @staticmethod
    def calculate_max_items(search_filters):
        transfer_target_max_items = 50
        max_items = int(transfer_target_max_items / len(search_filters))
        return max_items
