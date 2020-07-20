class SnipePlayer:
    def __init__(
        self,
        search_service,
        purchase_service,
        navigation_service,
        logging_service,
        database_service,
    ):
        self._search_service = search_service
        self._purchase_service = purchase_service
        self._navigation_service = navigation_service
        self._logging_service = logging_service
        self._database_service = database_service

    def execute(self, active_filter):
        self.search_market()

        result = self.purchase_first_player()

        if result == "player_purchased":
            self._logging_service.log(
                f"Player purchased!\n"
                f"Player name: {active_filter.name}\n"
                f"Listing player on transfer market...\n"
            )
            self.sell_player(active_filter)
        elif result == "no_player_found":
            self._logging_service.log("No player found...")
        elif result == "outbid_by_other_player":
            self._logging_service.log("Outbid by other player...")

        self.reset_search()

    def search_market(self):
        self._logging_service.log("Searching the transfer market")
        self._search_service.search()

    def purchase_first_player(self):
        if not self._purchase_service.buy_now():
            return "no_player_found"
        self._purchase_service.confirm_buy_now()

        if self._purchase_service.outbit_by_other_player():
            return "outbid_by_other_player"

        return "player_purchased"

    def sell_player(self, active_filter):
        self._purchase_service.list_on_transfer_market()
        purchase_price = self._purchase_service.get_purchase_price()
        profit = int(
            round((active_filter.sell_price * (0.95) - purchase_price) / 100, 0) * 100
        )

        self._purchase_service.set_start_price(active_filter.sell_price - 100)
        self._purchase_service.set_max_buy_now_price(active_filter.sell_price)
        self._purchase_service.list_item()

        self._logging_service.log("Player listed on transfer market!")
        self._database_service.save(
            name=active_filter.name,
            purchase_price=purchase_price,
            sell_price=active_filter.sell_price,
            profit=profit,
        )

    def reset_search(self):
        while self._navigation_service.get_location() != "SEARCH THE TRANSFER MARKET":
            self._navigation_service.go_back()
        self._search_service.reset_search()
