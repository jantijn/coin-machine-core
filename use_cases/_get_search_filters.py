from entities.search_filter import SearchFilter


class GetSearchFilters:
    def __init__(self, random_items, market_data, logger):
        self.random_items = random_items
        self.market_data = market_data
        self.logger = logger

    def execute(self, number_of_search_filters=1, margin=200, bonus=100):
        self.logger.log("Loading search filters")
        random_items = self.random_items.get(number_of_search_filters)
        search_filters = [self._item_to_search_filter(item, margin, bonus) for item in random_items]
        for search_filter in search_filters:
            self.logger.log(
                f"Loaded search filter --> name: {search_filter.name} \
                , buy price: {search_filter.buy_price} \
                , sell price: {search_filter.sell_price}"
            )
        return search_filters

    def _item_to_search_filter(self, item, margin, bonus):
        search_filter = SearchFilter(item["name"], margin, bonus)
        market_price = self.market_data.get_market_price(item["futbin_id"])
        search_filter.calculate_prices(market_price)
        return search_filter
