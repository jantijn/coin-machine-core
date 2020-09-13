from use_cases.bid_on_each_search_filter import BidOnEachSearchFilter
from use_cases.get_search_filters import GetSearchFilters
from use_cases.handle_error import HandleError
from use_cases.list_won_items import ListWonItems
from use_cases.refresh_transfer_list import RefreshTransferList
from use_cases.login import Login
from use_cases.responses import responses
from use_cases.verify_device import VerifyDevice


class Bot:
    def __init__(self, web_app, logger, market_data, repository):
        self.web_app = web_app
        self.logger = logger
        self.market_data = market_data
        self.repository = repository

    def login(self, username, password):
        login = Login(web_app=self.web_app, logger=self.logger)
        return login.execute(username, password)

    def verify_device(self, verification_code):
        verify_device = VerifyDevice(web_app=self.web_app, logger=self.logger)
        return verify_device.execute(verification_code=verification_code)

    def mass_bid(self, **kwargs):
        options = {
            "margin": 200,
            "bonus": 100,
            "number_of_repetitions": 6,
            "number_of_search_filters": 4,
            "max_time_left": 30,
        }
        options.update(kwargs)

        # try:
        self._run_mass_bid(options)
        # except Exception as exc:
        #     self.logger.log("Something went wrong")
        #     return responses.ResponseFailure.build_system_error(exc)
        return responses.ResponseSuccess()

    def _run_mass_bid(self, options):
        for repetition in range(options["number_of_repetitions"]):
            # try:
            self._run_mass_bid_cycle(options)
            # except Exception as exc:
            #     self._handle_error()

    def _run_mass_bid_cycle(self, options):
        self._refresh_transfer_list()
        search_filters = self._get_search_filters(
            number_of_search_filters=options["number_of_search_filters"],
            margin=options["margin"],
            bonus=options["bonus"],
        )
        self._bid_on_each_search_filter(search_filters, options["max_time_left"])
        self._list_won_items(search_filters)

    def _refresh_transfer_list(self):
        refresh_transfer_list = RefreshTransferList(
            web_app=self.web_app, logger=self.logger
        )
        return refresh_transfer_list.execute()

    def _get_search_filters(self, margin, bonus, number_of_search_filters):
        get_search_filters = GetSearchFilters(
            repository=self.repository, market_data=self.market_data, logger=self.logger
        )
        return get_search_filters.execute(number_of_search_filters, margin, bonus)

    def _bid_on_each_search_filter(self, search_filters, max_time_left):
        bid_on_each_search_filter = BidOnEachSearchFilter(
            web_app=self.web_app, logger=self.logger
        )
        return bid_on_each_search_filter.execute(search_filters, max_time_left)

    def _list_won_items(self, search_filters):
        list_won_items = ListWonItems(
            web_app=self.web_app, repository=self.repository, logger=self.logger
        )
        return list_won_items.execute(search_filters)

    def _handle_error(self):
        handle_error = HandleError(web_app=self.web_app, logger=self.logger)
        return handle_error.execute()
