import random
import time

from use_cases.bid_on_each_search_filter import BidOnEachSearchFilter
from use_cases.get_search_filters import GetSearchFilters
from use_cases.list_transfer_list_items import ListTransferListItems
from use_cases.list_won_items import ListWonItems
from use_cases.logout import Logout
from use_cases.refresh_transfer_list import RefreshTransferList
from use_cases.login import Login
from use_cases.responses import responses
from use_cases.snipe_item import SnipeItem
from use_cases.verify_device import VerifyDevice


class Bot:
    def __init__(self, web_app, logger, market_data, repository):
        self.web_app = web_app
        self.logger = logger
        self.market_data = market_data
        self.repository = repository
        self.username = None
        self.password = None

    def login(self):
        login = Login(web_app=self.web_app, logger=self.logger)
        return login.execute(self.username, self.password)

    def verify_device(self, verification_code):
        verify_device = VerifyDevice(web_app=self.web_app, logger=self.logger)
        return verify_device.execute(verification_code=verification_code)

    def mass_bid(self, **kwargs):
        options = {
            "margin": 200,
            "bonus": 100,
            "platform": "ps",
            "number_of_repetitions": 6,
            "number_of_search_filters": 4,
            "max_time_left": 0,
        }
        options.update(kwargs)

        # try:
        profit = self._run_mass_bid(options)
        # except Exception as exc:
        #     self.logger.log("Something went wrong")
        #     return responses.ResponseFailure.build_system_error(exc)
        self.logger.log(f"Bot finished successfully! Total profit is {profit}")
        return responses.ResponseSuccess()

    def _run_mass_bid(self, options):
        profit = 0
        for repetition in range(int(options["number_of_repetitions"])):
            profit += self._run_mass_bid_cycle(options)
        return profit

    def _run_mass_bid_cycle(self, options):
        self.bid_on_random_items(
            number_of_search_filters=options['number_of_search_filters'],
            margin=options["margin"],
            bonus=options["margin"],
            max_time_left=options["max_time_left"]
        )
        self._wait_until_bidding_finished(options["max_time_left"])
        return self.list_won_items(margin=options["margin"], bonus=options["bonus"])

    def bid_on_random_items(self, number_of_search_filters, margin, bonus, max_time_left):
        self._refresh_transfer_list()
        search_filters = self._get_search_filters(
            number_of_search_filters = number_of_search_filters,
            margin = margin,
            bonus = bonus
        )
        self._bid_on_each_search_filter(search_filters, max_time_left)

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

    def _wait_until_bidding_finished(self, max_time_left):
        if max_time_left == 0:
            return
        self.logger.log("Waiting until auctions with bid are finished...")
        pause_in_seconds = max_time_left * 60 + random.randint(1, 60)
        time.sleep(pause_in_seconds)

    def _logout(self):
        logout = Logout(web_app=self.web_app, logger=self.logger)
        logout.execute()

    def list_won_items(self, margin, bonus):
        list_won_items = ListWonItems(
            web_app=self.web_app, repository=self.repository, logger=self.logger
        )
        return list_won_items.execute(margin=margin, bonus=bonus)

    def list_transfer_list_items(self):
        list_transfer_list_items = ListTransferListItems(
            web_app=self.web_app, logger=self.logger, repository=self.repository, market_data=self.market_data
        )
        list_transfer_list_items.execute(type_of_item = 'available_items')
        self.logger.log("Bot finished successfully!")

    def list_expired_transfer_list_items(self):
        list_transfer_list_items = ListTransferListItems(
            web_app=self.web_app, logger=self.logger, repository=self.repository, market_data=self.market_data
        )
        list_transfer_list_items.execute(type_of_item = 'expired_items')
        self.logger.log("Bot finished successfully!")

    def snipe_item(self, characteristics, price, type_of_filter, number_of_attempts, success_action):
        snipe_item = SnipeItem(
            web_app=self.web_app, logger=self.logger, repository=self.repository, market_data=self.market_data
        )
        snipe_item.execute(
            characteristics = characteristics,
            price = price,
            number_of_attempts = number_of_attempts,
            type_of_filter = type_of_filter,
            success_action = success_action
        )
        self.logger.log("Bot finished successfully!")
