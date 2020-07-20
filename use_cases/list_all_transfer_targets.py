from difflib import SequenceMatcher


def calc_profit(purchase_price, sell_price):
    return round((sell_price * (0.95) - purchase_price) / 100, 0) * 100


def get_item_purchase_price(item_name, filters):
    return get_item_filter_data(item_name, filters).max_buy_now_price


def get_item_sell_price(item_name, filters):
    return get_item_filter_data(item_name, filters).sell_price


def get_item_filter_data(item_name, filters):
    if similar(item_name, filters[0].name) > similar(item_name, filters[1].name):
        return filters[0]
    else:
        return filters[1]


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


class ListAllTransferTargets:
    def __init__(self, fut_web_app_service, database_service, logging_service):
        self.fut_web_app_service = fut_web_app_service
        self.database_service = database_service
        self.logging_service = logging_service
        self.filters = []

    def execute(self, filters):
        self.filters = filters
        self._go_to_transfer_targets()
        self._clear_expired_players()
        self._list_all_won_items()

    def _go_to_transfer_targets(self):
        self.logging_service.log('Going to the transfer targets')
        self.fut_web_app_service.navigation_service.go_to_transfers()
        self.fut_web_app_service.navigation_service.go_to_transfer_targets()

    def _clear_expired_players(self):
        self.logging_service.log('Clearing expired players')
        self.fut_web_app_service.transfer_target_service.clear_expired_players()

    def _list_all_won_items(self):
        self.logging_service.log('Listing all won items')
        won_items = self.fut_web_app_service.transfer_target_service.get_won_items()

        while len(won_items) > 1:
            try:
                item = self.fut_web_app_service.transfer_target_service.select(won_items[0])
                self._list_item(item)
            except:
                pass
            won_items = self.fut_web_app_service.transfer_target_service.get_won_items()

    def _list_item(self, item):
        name = self.fut_web_app_service.transfer_target_service.get_item_name(item)
        purchase_price = get_item_purchase_price(name, self.filters)
        sell_price = get_item_sell_price(name, self.filters)
        profit = calc_profit(purchase_price = purchase_price, sell_price = sell_price),

        print('Listing ' + name)
        self.fut_web_app_service.transfer_target_service.list_on_transfer_market()
        self.fut_web_app_service.transfer_target_service.set_start_price(sell_price - 100)
        self.fut_web_app_service.transfer_target_service.set_max_buy_now_price(sell_price)
        self.fut_web_app_service.transfer_target_service.list_item()
        self.database_service.save(
            name = name,
            purchase_price = purchase_price,
            sell_price = sell_price,
            profit = profit
        )
