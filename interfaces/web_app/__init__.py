from selenium.common.exceptions import StaleElementReferenceException

from use_cases.exceptions.exceptions import (
    WrongCredentialsException,
    WrongVerificationCodeError,
)
from .pages import (
    general,
    home,
    login,
    search_results,
    search_the_market,
    sidebar,
    transfer_list,
    transfer_targets,
    transfers,
    verify_device,
    settings,
)
from interfaces.web_app.pages.general import initialize
from .purchased_item import PurchasedItem
from .transfer_list_item import TransferListItem


class WebApp:
    def __init__(self, headless=True, verbose=False, custom_driver=False):
        if not custom_driver:
            self.driver = initialize(headless)
        self.verbose = verbose

    def set_driver(self, driver):
        self.driver = driver

    def login_required(self):
        return login.login_required(self.driver)

    def login(self, email=None, password=None):
        login.go_to_login(self.driver, self.verbose)
        if login.credentials_required(self.driver):
            self._enter_credentials(email, password)
        else:
            self._clear_home_screen()

    def _enter_credentials(self, email, password):
        login.enter_credentials(self.driver, email, password, self.verbose)
        login.confirm_credentials(self.driver, self.verbose)
        if login.wrong_credentials(self.driver, self.verbose):
            raise WrongCredentialsException("Wrong email address or password")
        if login.verification_code_required(self.driver, self.verbose):
            login.request_verification_code(self.driver, self.verbose)
        else:
            self._clear_home_screen()

    def verify_device(self, verification_code):
        verify_device.enter_verification_code(self.driver, verification_code)
        verify_device.confirm_verification_code(self.driver)
        if verify_device.wrong_verification_code(self.driver):
            raise WrongVerificationCodeError("Wrong verification code")
        self._clear_home_screen()

    def refresh(self):
        general.refresh(self.driver)
        home.wait_until_loaded(self.driver)
        self._clear_home_screen()

    def _clear_home_screen(self):
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

    def go_to_search_the_transfer_market(self):
        sidebar.go_to_transfers(self.driver)
        transfers.go_to_search_the_transfer_market(self.driver)

    def set_filter(self, name, price, strategy):
        if strategy == 'bid':
            search_the_market.set_bid_filter(self.driver, name, price)
        elif strategy == 'snipe':
            search_the_market.set_snipe_filter(self.driver, name, price)

    def set_filter_based_on_characteristics(self, club, nation, position, price):
        search_the_market.set_snipe_filter_based_on_characteristics(
            self.driver, club, nation, position, price
        )

    def increment_min_bid_price(self):
        search_the_market.increment_min_bid_price(self.driver)

    def decrement_min_bid_price(self):
        search_the_market.decrement_min_bid_price(self.driver)

    def search(self):
        search_the_market.search_the_transfer_market(self.driver)

    def go_back(self):
        search_the_market.go_back(self.driver)

    def set_min_bid_price(self, price):
        search_the_market.set_min_bid_price(self.driver, price)

    def bid_on_search_filter_items(self, search_filter, max_items, max_time_left):
        search_results.bid_on_search_results(
            self.driver, search_filter.buy_price, max_items, max_time_left
        )

    def snipe_item(self):
        if not search_results.buy_now(self.driver):
            return ['no_item_found', None]
        search_results.confirm_buy_now(self.driver)

        if search_results.outbid_by_other_player(self.driver):
            return ['outbid', None]

        name = search_results.get_name(self.driver)
        purchase_price = search_results.get_purchase_price(self.driver)

        return ['success', {'name': name, 'purchase_price': purchase_price}]

    def send_to_club(self):
        search_results.send_to_club(self.driver)

    def send_to_transfer_list(self):
        search_results.send_to_transfer_list(self.driver)

    def list(self, price):
        search_results.list(self.driver, price)

    def go_to_transfer_targets(self):
        sidebar.go_to_transfers(self.driver)
        transfers.go_to_transfer_targets(self.driver)

    def get_purchased_items(self):
        if not sidebar.get_location(self.driver) == "TRANSFER TARGETS":
            self.go_to_transfer_targets()
        transfer_targets.clear_expired_players(self.driver)
        won_items = transfer_targets.get_won_items(self.driver)
        return [
            PurchasedItem(web_app_element) for web_app_element in won_items
        ]

    def go_to_transfer_list(self):
        sidebar.go_to_transfers(self.driver)
        transfers.go_to_transfer_list(self.driver)

    def get_transfer_list_items(self, type_of_item):
        if not sidebar.get_location(self.driver) == "TRANSFER LIST":
            self.go_to_transfer_list()

        transfer_list_items = transfer_list.get_available_items(self.driver, type_of_item)
        return [
            TransferListItem(web_app_element) for web_app_element in transfer_list_items
        ]

    def logout(self):
        sidebar.go_to_settings(self.driver)
        settings.logout(self.driver)
        settings.confirm_logout(self.driver)
