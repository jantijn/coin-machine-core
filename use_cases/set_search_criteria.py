class SetSearchCriteria:
    def __init__(self, navigation_service, search_service):
        self._navigation_service = navigation_service
        self._search_service = search_service

    def execute(self, active_filter, bid=False):
        self._go_to_transfer_market()
        if bid:
            self._set_bid_filter(active_filter)
        else:
            self._set_buy_now_filter(active_filter)

    def _go_to_transfer_market(self):
        self._navigation_service.go_to_transfers()
        self._navigation_service.go_to_search_the_transfer_market()

    def _set_buy_now_filter(self, active_filter):
        self._search_service.set_player_name(active_filter.name)
        self._search_service.set_max_buy_now_price(active_filter.max_buy_now_price)
        self._search_service.set_min_bid_price(150)

    def _set_bid_filter(self, active_filter):
        self._search_service.set_player_name(active_filter.name)
        self._search_service.set_max_bid_price(active_filter.max_buy_now_price)
