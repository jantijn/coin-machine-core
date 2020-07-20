from entities.search_filter_entity import SearchFilterEntity


class GetFilters:
    def __init__(self, database_service, market_price_service, logging_service):
        self.database_service = database_service
        self.market_price_service = market_price_service
        self.logging_service = logging_service

    def execute(self):
        self.logging_service.log('Getting search filters')
        search_filters = []
        items = self.database_service.getRandomItems(number = 2)
        for item in items:
            self.logging_service.log('Picked item: ' + item.name)
            search_filter = SearchFilterEntity.from_dict(item)
            search_filter.calculate_prices(self._market_price_service.get(filter.futbin_id))
            search_filters.append(filter)
        return search_filters
