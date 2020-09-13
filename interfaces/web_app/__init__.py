from selenium.common.exceptions import StaleElementReferenceException

from entities.purchased_item import PurchasedItem
from use_cases.exceptions.exceptions import (
    WrongCredentialsException,
    WrongVerificationCodeError,
)
from . import (
    login,
    search_results,
    verify_device,
    general,
    transfer_list,
    search_the_market,
    home,
    sidebar,
    transfers,
    transfer_targets,
)
from interfaces.web_app.general import initialize


class WebApp:
    def __init__(self, headless=True, verbose=False):
        self.driver = initialize(headless)
        self.verbose = verbose

    def set_driver(self, driver):
        self.driver = driver

    def login(self, email, password):
        login.go_to_login(self.driver, self.verbose)
        login.enter_credentials(self.driver, email, password, self.verbose)
        login.confirm_credentials(self.driver, self.verbose)
        if login.wrong_credentials(self.driver, self.verbose):
            raise WrongCredentialsException("Wrong email address or password")
        if login.verification_code_required(self.driver, self.verbose):
            login.request_verification_code(self.driver, self.verbose)

    def verify_device(self, verification_code):
        verify_device.enter_verification_code(self.driver, verification_code)
        verify_device.confirm_verification_code(self.driver)
        if verify_device.wrong_verification_code(self.driver):
            raise WrongVerificationCodeError("Wrong verification code")
        home.wait_until_loaded(self.driver)
        home.handle_pop_ups(self.driver)

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

    def bid_on_search_filter_items(self, search_filter, max_items, max_time_left):
        sidebar.go_to_transfers(self.driver)
        transfers.go_to_search_the_transfer_market(self.driver)
        search_the_market.set_bid_filter(
            self.driver, search_filter.name, search_filter.buy_price
        )
        search_the_market.search_the_transfer_market(self.driver)
        search_results.bid_on_search_results(
            self.driver, search_filter.buy_price, max_items, max_time_left
        )

    def list_all_won_items(self, search_filters):
        sidebar.go_to_transfers(self.driver)
        transfers.go_to_transfer_targets(self.driver)
        transfer_targets.clear_expired_players(self.driver)
        purchased_items = transfer_targets.list_all_won_items(
            self.driver, search_filters
        )
        return [PurchasedItem.from_dict(item) for item in purchased_items]

    def refresh(self):
        general.refresh(self.driver)
        home.wait_until_loaded(self.driver)
