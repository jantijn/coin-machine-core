import time
from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

class ListAllTransferTargets:
    def __init__(self, transfer_target_service, navigation_service, logging_service, purchase_service):
        self._transfer_target_service = transfer_target_service
        self._navigation_service = navigation_service
        self._purchase_service = purchase_service
        self._logging_service = logging_service

    def execute(self, filters):
        self._go_to_transfer_targets()
        self._clear_expired_players()
        self._list_all_won_items(filters)

    def _go_to_transfer_targets(self):
        self._navigation_service.go_to_transfers()
        self._navigation_service.go_to_transfer_targets()

    def _clear_expired_players(self):
        print('clearing')
        self._transfer_target_service.clear_expired_players()

    def _list_all_won_items(self, filters):
        won_items = self._transfer_target_service.get_won_items()

        while len(won_items) > 1:
            try:
                item = self._transfer_target_service.select(won_items[0])
                item_name = self._transfer_target_service.get_item_name(item)
                sell_price = self._get_item_sell_price(item_name, filters)
                self._list_item(item_name, sell_price)
            except:
                pass
            won_items = self._transfer_target_service.get_won_items()

    def _get_item_sell_price(self, item_name, filters):
        if similar(item_name, filters[0].name) > similar(item_name, filters[1].name):
            return filters[0].sell_price
        else:
            return filters[1].sell_price

    def _list_item(self, item_name, sell_price):        
        print('listing ' + item_name)
        self._transfer_target_service.list_on_transfer_market()
        self._transfer_target_service.set_start_price(sell_price - 100)
        self._transfer_target_service.set_max_buy_now_price(sell_price)
        self._transfer_target_service.list_item()

