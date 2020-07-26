import time
import random
from difflib import SequenceMatcher

from . import selectors
from use_cases.exceptions.exceptions import WrongCredentialsError, WrongVerificationCodeError
from .web_app_objects import (
    WebAppObject,
    ClickableWebAppObject,
    FillableWebAppObject,
    SearchResultList,
    WonItemList,
)


class Executor:
    def __init__(self, driver):
        self.driver = driver


class SideBarMixin:
    def __init__(self):
        self.driver = None

    def _go_to_transfers(self):
        go_to_transfers_button = ClickableWebAppObject.from_selector(
            self.driver, selectors.GO_TO_TRANSFERS_BUTTON
        )
        go_to_transfers_button.safe_click()


class LoginExecutor(Executor):
    def login(self, email, password):
        self._go_to_login()
        self._enter_credentials(email, password)
        self._confirm_credentials()
        if self._wrong_credentials():
            raise WrongCredentialsError("Wrong email address or password")
        if self._verification_code_required():
            self._request_verification_code()

    def _go_to_login(self):
        go_to_login_button = ClickableWebAppObject.from_selector(
            self.driver, selectors.GO_TO_LOGIN_BUTTON
        )
        go_to_login_button.slow_click()

    def _enter_credentials(self, email, password):
        email_field = FillableWebAppObject.from_selector(
            self.driver, selectors.EMAIL_FIELD
        )
        email_field.fill(email)

        password_field = FillableWebAppObject.from_selector(
            self.driver, selectors.PASSWORD_FIELD
        )
        password_field.fill(password)

    def _confirm_credentials(self):
        confirm_credentials_button = ClickableWebAppObject.from_selector(
            self.driver, selectors.CONFIRM_CREDENTIALS_BUTTON
        )
        confirm_credentials_button.slow_click()

    def _wrong_credentials(self):
        wrong_credentials_label = WebAppObject.from_selector(
            self.driver, selectors.WRONG_CREDENTIALS_NOTIFICATION
        )
        return wrong_credentials_label.is_present()

    def _verification_code_required(self):
        verification_code_button = ClickableWebAppObject.from_selector(
            self.driver, selectors.REQUEST_VERIFICATION_CODE_BUTTON
        )
        return verification_code_button.is_present()

    def _request_verification_code(self):
        verification_code_button = ClickableWebAppObject.from_selector(
            self.driver, selectors.REQUEST_VERIFICATION_CODE_BUTTON
        )
        verification_code_button.slow_click()


class VerifyDeviceExecutor(Executor):
    def verify_device(self, verification_code):
        self._enter_verification_code(verification_code)
        self._confirm_verification_code()
        if self._wrong_verification_code():
            raise WrongVerificationCodeError("Wrong verification code")

    def _enter_verification_code(self, verification_code):
        verification_code_field = FillableWebAppObject.from_selector(
            self.driver, selectors.VERIFICATION_CODE_FIELD
        )
        verification_code_field.fill(verification_code)

    def _confirm_verification_code(self):
        verification_code_button = ClickableWebAppObject.from_selector(
            self.driver, selectors.CONFIRM_VERIFICATION_CODE_BUTTON
        )
        verification_code_button.slow_click()

    def _wrong_verification_code(self):
        wrong_credentials_label = WebAppObject.from_selector(
            self.driver, selectors.WRONG_VERIFICATION_CODE
        )
        return wrong_credentials_label.is_present()


class RefreshTransferListExecutor(Executor, SideBarMixin):
    def refresh_transfer_list(self):
        self._go_to_transfers()
        self._go_to_transfer_list()
        self._remove_sold_items()
        self._relist_unsold_items()

    def _go_to_transfer_list(self):
        go_to_transfers_button = ClickableWebAppObject.from_selector(
            self.driver, selectors.GO_TO_TRANSFER_LIST_BUTTON
        )
        go_to_transfers_button.safe_click()

    def _remove_sold_items(self):
        go_to_transfers_button = ClickableWebAppObject.from_selector(
            self.driver, selectors.REMOVE_SOLD_ITEMS_BUTTON
        )
        go_to_transfers_button.slow_click()

    def _relist_unsold_items(self):
        relist_unsold_items_button = ClickableWebAppObject.from_selector(
            self.driver, selectors.RELIST_UNSOLD_ITEMS_BUTTON
        )
        relist_unsold_items_button.slow_click()

        confirm_relist_button = ClickableWebAppObject.from_selector(
            self.driver, selectors.CONFIRM_RELIST_BUTTON
        )
        confirm_relist_button.slow_click()


class BidOnSearchFilterItemsExecutor(Executor, SideBarMixin):
    def bid_on_search_filter_items(self, search_filter, max_items=20, max_time_left=60):
        self._go_to_transfers()
        self._go_to_search_the_transfer_market()
        self._set_bid_filter(search_filter.name, search_filter.buy_price)
        self._search_the_transfer_market()
        self._bid_on_items(search_filter.buy_price, max_items, max_time_left)

    def _go_to_search_the_transfer_market(self):
        go_to_search_the_transfer_market_button = ClickableWebAppObject.from_selector(
            self.driver, selectors.GO_TO_SEARCH_THE_TRANSFER_MARKET_BUTTON
        )
        go_to_search_the_transfer_market_button.safe_click()

    def _set_bid_filter(self, name, price):
        name_field = FillableWebAppObject.from_selector(
            self.driver, selectors.NAME_FIELD
        )
        name_field.fill(name)

        name_button = ClickableWebAppObject.from_selector(
            self.driver, selectors.NAME_BUTTON
        )
        name_button.slow_click()

        max_bid_price_field = FillableWebAppObject.from_selector(
            self.driver, selectors.MAX_BID_PRICE_FIELD
        )
        max_bid_price_field.fill(price)

    def _search_the_transfer_market(self):
        search_the_transfer_market_button = ClickableWebAppObject.from_selector(
            self.driver, selectors.SEARCH_THE_TRANSFER_MARKET_BUTTON
        )
        search_the_transfer_market_button.slow_click()

    def _bid_on_items(self, price, max_items, max_time_left):
        number_of_items_bid_on = 0
        search_results = SearchResultList.from_selector(
            self.driver, selectors.SEARCH_RESULTS
        )
        for item in search_results.get_all():
            self._random_pause(1)
            if number_of_items_bid_on >= max_items:
                break
            if item.get_time_left() >= max_time_left:
                break
            item.bid(price)
            number_of_items_bid_on = number_of_items_bid_on + 1

    @staticmethod
    def _random_pause(average_pause_time_in_seconds):
        time.sleep(average_pause_time_in_seconds + random.uniform(-0.5, 0.5))


class ListAllTransferTargetsExecutor(Executor, SideBarMixin):
    def list_all_transfer_targets(self, search_filters):
        self._go_to_transfers()
        self._go_to_transfer_targets()
        self._clear_expired_players()
        self._list_all_won_items(search_filters)

    def _go_to_transfer_targets(self):
        go_to_transfer_targets_button = ClickableWebAppObject.from_selector(
            self.driver, selectors.GO_TO_TRANSFER_TARGETS_BUTTON
        )
        go_to_transfer_targets_button.safe_click()

    def _clear_expired_players(self):
        clear_expired_players_button = ClickableWebAppObject.from_selector(
            self.driver, selectors.CLEAR_EXPIRED_PLAYERS_BUTTON
        )
        clear_expired_players_button.slow_click()

    def _list_all_won_items(self, search_filters):
        won_item_list = WonItemList.from_selector(self.driver, selectors.WON_ITEMS)
        while len(won_item_list) > 0:
            won_item = won_item_list.pop_first()
            sell_price = self._get_sell_price(won_item.get_name(), search_filters)
            won_item.list(sell_price)

    def _get_sell_price(self, item_name, search_filters):
        matching_filter = self._get_matching_filter(item_name, search_filters)
        return matching_filter.sell_price

    @staticmethod
    def _get_matching_filter(item_name, search_filters):
        max_similar_score = 0
        matching_filter = {}
        for search_filter in search_filters:
            similar_score = SequenceMatcher(None, item_name, search_filter.name).ratio()
            if similar_score > max_similar_score:
                matching_filter = search_filter
                max_similar_score = similar_score
        return matching_filter

