from use_cases.handle_error import HandleError


class BidOnSearchFilter:
    def __init__(self, web_app, logger):
        self.web_app = web_app
        self.logger = logger

    def execute(self, search_filter, max_items, max_time_left):
        try:
            items_with_bid = self._bid_on_search_filter(
                search_filter, max_items, max_time_left
            )
        except Exception as e:
            self._handle_error(e)
            items_with_bid = 0
        return items_with_bid

    def _bid_on_search_filter(self, search_filter, max_items, max_time_left):
        self.logger.log(f"Bidding on {search_filter.name}...")
        self._search_filter(search_filter)
        number_of_bids_placed = self._bid_on_search_results(
            max_items, max_time_left, search_filter
        )
        self.logger.log(f"Finished bidding on {search_filter.name}")
        return number_of_bids_placed

    def _search_filter(self, search_filter):
        self.web_app.navigator.go_to_search_the_transfer_market()
        self.web_app.search_filter.fill(
            name=search_filter.name, price=search_filter.buy_price
        )
        self.web_app.search_filter.search()

    def _bid_on_search_results(self, max_items, max_time_left, search_filter):
        number_of_bids_placed = 0
        search_results = self.web_app.search_results.get_all()
        for search_result in search_results:
            if search_result.time_left >= max_time_left:
                break
            if number_of_bids_placed >= max_items:
                break
            search_result.bid(search_filter.buy_price)
            self.logger.log(f"Placed bid")
            number_of_bids_placed += 1
        return number_of_bids_placed

    def _handle_error(self, e):
        handle_error = HandleError(web_app=self.web_app, logger=self.logger)
        handle_error.execute(e)
