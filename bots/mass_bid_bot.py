from use_cases.bid_on_each_search_filter import BidOnEachSearchFilter
from use_cases.get_search_filters import GetSearchFilters
from use_cases.list_won_items import ListWonItems
from use_cases.login import Login
from use_cases.refresh_transfer_list import RefreshTransferList
from use_cases.verify_device import VerifyDevice


class MassBidBot:
    def __init__(self, web_app, random_items, market_data, purchased_items, logger):
        self.web_app = web_app
        self.random_items = random_items
        self.market_data = market_data
        self.purchased_items = purchased_items
        self.logger = logger

    def login(self, username, password):
        login = Login(self.web_app, self.logger)
        return login.execute(username, password)

    def verify_device(self, verification_code):
        verify_device = VerifyDevice(self.web_app, self.logger)
        return verify_device.execute(verification_code)

    def mass_bid(self, **kwargs):
        options = {
            "margin": 200,
            "bonus": 100,
            "number_of_repetitions": 1,
            "number_of_search_filters": 1,
            "max_time_left": 5,
        }
        options.update(kwargs)

        for repetition in range(options["number_of_repetitions"]):
            self._refresh_transfer_list()
            search_filters = self._get_search_filters(
                options["number_of_search_filters"], options["margin"], options["bonus"]
            )
            self._bid_on_each_search_filter(
                search_filters, options["max_time_left"]
            )
            self._list_won_items(search_filters)

    def _refresh_transfer_list(self):
        refresh_transfer_list = RefreshTransferList(self.web_app, self.logger)
        return refresh_transfer_list.execute()

    def _get_search_filters(self, margin, bonus, number_of_search_filters):
        get_search_filters = GetSearchFilters(
            self.random_items, self.market_data, self.logger
        )
        return get_search_filters.execute(number_of_search_filters, margin, bonus)

    def _bid_on_each_search_filter(self, search_filters, max_time_left):
        bid_on_each_search_filter = BidOnEachSearchFilter(self.web_app, self.logger)
        return bid_on_each_search_filter.execute(search_filters, max_time_left)

    def _list_won_items(self, search_filters):
        list_won_items = ListWonItems(self.web_app, self.purchased_items, self.logger)
        return list_won_items.execute(search_filters)
