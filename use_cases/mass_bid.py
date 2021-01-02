import random
import time

from use_cases.bid_on_search_filter import BidOnSearchFilter
from use_cases.get_search_filters import GetSearchFilters
from use_cases.list_won_items import ListWonItems
from use_cases.refresh_transfer_list import RefreshTransferList


class MassBid:
    def __init__(self, web_app, repository, logger):
        self.web_app = web_app
        self.repository = repository
        self.logger = logger

    def execute(
        self, margin=300, bonus=0, repetitions=1, max_total=30, max_time_left=5, max_per_cycle=15
    ):
        profit = 0
        for i in range(int(repetitions)):
            profit += self._mass_bid(
                margin=margin,
                bonus=bonus,
                max_total=max_total,
                max_time_left=max_time_left,
                max_per_cycle=max_per_cycle
            )
        self.logger.log(f"Total profit: {profit}")
        return profit

    def _mass_bid(self, margin, bonus, max_total, max_time_left, max_per_cycle):
        number_of_bids_placed = 0
        self._refresh_transfer_list()
        while number_of_bids_placed < max_total:
            search_filter = self._get_search_filter(margin, bonus)
            number_of_bids_placed += self._bid_on_search_filter(
                search_filter, max_per_cycle, max_time_left
            )
        self._wait_until_bidding_finished(max_time_left)
        profit = self._list_won_items(margin, bonus)
        return profit

    def _refresh_transfer_list(self):
        refresh_transfer_list = RefreshTransferList(
            web_app=self.web_app, logger=self.logger
        )
        return refresh_transfer_list.execute()

    def _get_search_filter(self, margin, bonus):
        get_search_filters = GetSearchFilters(
            repository=self.repository, logger=self.logger
        )
        return get_search_filters.execute(
            number_of_search_filters=1, margin=margin, bonus=bonus
        )[0]

    def _bid_on_search_filter(self, search_filter, max_per_cycle, max_time_left):
        bid_on_search_filter = BidOnSearchFilter(
            web_app=self.web_app, logger=self.logger
        )
        return bid_on_search_filter.execute(search_filter, max_per_cycle, max_time_left)

    def _wait_until_bidding_finished(self, max_time_left):
        if max_time_left == 0:
            return
        self.logger.log("Waiting until auctions with bid are finished...")
        pause_in_seconds = max_time_left * 60 + random.randint(1, 60)
        time.sleep(pause_in_seconds)

    def _list_won_items(self, margin, bonus):
        list_won_items = ListWonItems(
            web_app=self.web_app, repository=self.repository, logger=self.logger
        )
        return list_won_items.execute(margin=margin, bonus=bonus)
