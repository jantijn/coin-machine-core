class GetSearchFilters:
    def __init__(self, repository, market_data, logger):
        self.repository = repository
        self.market_data = market_data
        self.logger = logger

    def execute(self, number_of_search_filters=1, margin=200, bonus=100, platform="ps"):
        self.logger.log("Loading search filters")
        search_filters = self.repository.get_random_search_filters(number_of_search_filters)

        for search_filter in search_filters:
            search_filter.calculate_prices(margin=margin, bonus=bonus)
            self.logger.log(
                f"Loaded search filter --> name: {search_filter.name} \
                , buy price: {search_filter.buy_price} \
                , sell price: {search_filter.sell_price}"
            )
        return search_filters
