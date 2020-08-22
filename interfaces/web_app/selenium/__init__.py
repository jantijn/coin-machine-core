from selenium.common.exceptions import StaleElementReferenceException

from entities.purchased_item import PurchasedItem
from use_cases.exceptions.exceptions import WrongCredentialsException, WrongVerificationCodeError
from . import (
    _app,
    _home,
    _login,
    _search_results,
    _search_the_market,
    _sidebar,
    _transfer_list,
    _transfer_targets,
    _transfers,
    _verify_device,
)


class WebAppInterface:
    def __init__(self, driver=None, verbose=False):
        self.driver = driver
        self.verbose = verbose

    def set_driver(self, driver):
        self.driver = driver

    def login(self, email, password):
        _login.go_to_login(self.driver, self.verbose)
        _login.enter_credentials(self.driver, email, password, self.verbose)
        _login.confirm_credentials(self.driver, self.verbose)
        if _login.wrong_credentials(self.driver, self.verbose):
            raise WrongCredentialsException("Wrong email address or password")
        if _login.verification_code_required(self.driver, self.verbose):
            _login.request_verification_code(self.driver, self.verbose)

    def verify_device(self, verification_code):
        _verify_device.enter_verification_code(self.driver, verification_code)
        _verify_device.confirm_verification_code(self.driver)
        if _verify_device.wrong_verification_code(self.driver):
            raise WrongVerificationCodeError("Wrong verification code")
        _home.wait_until_loaded(self.driver)
        _home.handle_pop_ups(self.driver)

    def refresh_transfer_list(self):
        try:
            self._refresh_transfer_list()
        except StaleElementReferenceException:
            self.refresh_transfer_list()

    def _refresh_transfer_list(self):
        _sidebar.go_to_transfers(self.driver)
        _transfers.go_to_transfer_list(self.driver)
        _transfer_list.remove_sold_items(self.driver)
        _transfer_list.relist_unsold_items(self.driver)

    def bid_on_search_filter_items(self, search_filter, max_items, max_time_left):
        _sidebar.go_to_transfers(self.driver)
        _transfers.go_to_search_the_transfer_market(self.driver)
        _search_the_market.set_bid_filter(self.driver, search_filter.name, search_filter.buy_price)
        _search_the_market.search_the_transfer_market(self.driver)
        _search_results.bid_on_search_results(self.driver, search_filter.buy_price, max_items, max_time_left)

    def list_all_won_items(self, search_filters):
        _sidebar.go_to_transfers(self.driver)
        _transfers.go_to_transfer_targets(self.driver)
        _transfer_targets.clear_expired_players(self.driver)
        purchased_items = _transfer_targets.list_all_won_items(self.driver, search_filters)
        return [PurchasedItem.from_dict(item) for item in purchased_items]

    def refresh(self):
        _app.refresh(self.driver)
        _home.wait_until_loaded(self.driver)
