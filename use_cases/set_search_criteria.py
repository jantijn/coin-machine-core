class SetSearchCriteria:
    def __init__(self, fut_web_app_service, logging_service):
        self.fut_web_app_service = fut_web_app_service
        self.logging_service = logging_service

    def execute(self, active_filter, bid=False):
        self.fut_web_app_service.go_to_transfer_market()
        if bid:
            self._set_bid_filter(active_filter)
        else:
            self._set_buy_now_filter(active_filter)

    def _go_to_transfer_market(self):
        self.logging_service.log('Going to transfer market')
        self.fut_web_app_service.navigation_service.go_to_transfers()
        self.fut_web_app_service.navigation_service.go_to_search_the_transfer_market()

    def _set_buy_now_filter(self, active_filter):
        self.fut_web_app_service.search_service.set_player_name(active_filter.name)
        self.fut_web_app_service.search_service.set_max_buy_now_price(active_filter.max_buy_now_price)
        self.fut_web_app_service.search_service.set_min_bid_price(150)
        self.logging_service.log('Search filter set')

    def _set_bid_filter(self, active_filter):
        self.fut_web_app_service.search_service.set_player_name(active_filter.name)
        self.fut_web_app_service.search_service.set_max_bid_price(active_filter.max_buy_now_price)
        self.logging_service.log('Search filter set')
