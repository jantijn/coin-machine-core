from selenium.common.exceptions import StaleElementReferenceException

from interfaces.web_app.login import Login
from interfaces.web_app.navigator import Navigator
from interfaces.web_app.pages import sidebar, transfers, transfer_list
from interfaces.web_app.pages.general import initialize
from interfaces.web_app.search_filter import SearchFilter
from interfaces.web_app.search_results import SearchResults
from interfaces.web_app.transfer_list_item import TransferListItems
from interfaces.web_app.won_item import WonItems


class WebApp:
    def __init__(self, headless=True, verbose=False, custom_driver=False):
        if not custom_driver:
            self.driver = initialize(headless)
            self.create_classes()
        self.verbose = verbose

    def set_driver(self, driver):
        self.driver = driver
        self.create_classes()

    def create_classes(self):
        self.login = Login(driver=self.driver)
        self.navigator = Navigator(driver=self.driver)
        self.search_filter = SearchFilter(driver=self.driver)
        self.search_results = SearchResults(driver=self.driver)
        self.won_items = WonItems(driver=self.driver)
        self.transfer_list_items = TransferListItems(driver=self.driver)

    def refresh_transfer_list(self):
        try:
            self._refresh_transfer_list()
        except StaleElementReferenceException:
            self.refresh_transfer_list()

    def _refresh_transfer_list(self):
        sidebar.go_to_transfers(self.driver)
        transfers.go_to_transfer_list(self.driver)
        transfer_list.remove_sold_items(self.driver)
        transfer_list.relist_unsold_items(self.driver)
