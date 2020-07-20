from entities.search_filter_entity import SearchFilterEntity


class GetFilters:
    def __init__(self, market_price_service, player_service):
        self._market_price_service = market_price_service
        self._player_service = player_service

    def execute(self):
        filters = []
        items = self._player_service.get()
        for item in items:
            filter = SearchFilterEntity.from_dict(item)
            filter.calculate_prices(self._market_price_service.get(filter.futbin_id))
            filters.append(filter)
        return filters
