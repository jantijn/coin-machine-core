import collections

from interfaces.logger.console import LoggerInterface
from interfaces.market_data.futbin import MarketDataInterface
from interfaces.purchased_items.ignore import PurchasedItemInterface
from interfaces.random_items.in_memory import RandomItemsInterface
from interfaces.web_app.selenium import WebAppInterface

from use_cases._bid_on_each_search_filter import BidOnEachSearchFilter
from use_cases._get_search_filters import GetSearchFilters
from use_cases._list_won_items import ListWonItems
from use_cases._refresh_transfer_list import RefreshTransferList
from use_cases.login import Login
from use_cases.verify_device import VerifyDevice


web_app = WebAppInterface()
random_items = RandomItemsInterface()
market_data = MarketDataInterface()
purchased_items = PurchasedItemInterface()
logger = LoggerInterface()

UseCases = collections.namedtuple('UseCases', 'login verify_device, bid_on_each_search_filter, get_search_filters, '
                                                'list_won_items refresh_transfer_list')


def build_use_cases(driver_):
    web_app.set_driver(driver_)

    login = Login(web_app, logger).execute
    verify_device = VerifyDevice(web_app, logger).execute
    bid_on_each_search_filters = BidOnEachSearchFilter(web_app, logger).execute
    get_search_filters = GetSearchFilters(random_items, market_data, logger).execute
    list_won_items = ListWonItems(web_app, purchased_items, logger).execute
    refresh_transfer_list = RefreshTransferList(web_app, logger)

    return UseCases(login, verify_device, bid_on_each_search_filters, get_search_filters, list_won_items, refresh_transfer_list)