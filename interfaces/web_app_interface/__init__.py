from interfaces.web_app_interface import selectors
from interfaces.web_app_interface.exceptions import WrongCredentialsError, WrongVerificationCodeError
from interfaces.web_app_interface.utils import Button, InputField, Label, random_pause, List, Item


class WebAppInterface:
    
    def __init__(self, driver):
        self.driver = driver

    def login(self, email, password):
        self._go_to_login()
        self._enter_credentials(email, password)
        self._confirm_credentials()
        if self._wrong_credentials():
            raise WrongCredentialsError('Wrong email address or password')
        if self._verification_code_required():
            self._request_verification_code()

    def _go_to_login(self):
        go_to_login_button = Button(self.driver, selectors.GO_TO_LOGIN_BUTTON)
        go_to_login_button.slow_click()

    def _enter_credentials(self, email, password):
        email_field = InputField(self.driver, selectors.EMAIL_FIELD)
        email_field.fill(email)

        password_field = InputField(self.driver, selectors.PASSWORD_FIELD)
        password_field.fill(password)

    def _confirm_credentials(self):
        confirm_credentials_button = Button(self.driver, selectors.CONFIRM_CREDENTIALS_BUTTON)
        confirm_credentials_button.slow_click()

    def _wrong_credentials(self):
        wrong_credentials_label = Label(self.driver, selectors.WRONG_CREDENTIALS_NOTIFICATION)
        return wrong_credentials_label.is_present()

    def _verification_code_required(self):
        verification_code_button = Button(self.driver, selectors.REQUEST_VERIFICATION_CODE_BUTTON)
        return verification_code_button.is_present()

    def _request_verification_code(self):
        verification_code_button = Button(self.driver, selectors.REQUEST_VERIFICATION_CODE_BUTTON)
        verification_code_button.slow_click()

    def verify_device(self, verification_code):
        self._enter_verification_code(verification_code)
        self._confirm_verification_code()
        if self._wrong_verification_code():
            raise WrongVerificationCodeError('Wrong verification code')

    def _enter_verification_code(self, verification_code):
        verification_code_field = InputField(self.driver, selectors.EMAIL_FIELD)
        verification_code_field.fill(verification_code)

    def _confirm_verification_code(self):
        verification_code_button = Button(self.driver, selectors.CONFIRM_VERIFICATION_CODE_BUTTON)
        verification_code_button.slow_click()

    def _wrong_verification_code(self):
        wrong_credentials_label = Label(self.driver, selectors.WRONG_VERIFICATION_CODE)
        return wrong_credentials_label.is_present()

    def set_search_criteria(self, name, price):
        self._go_to_transfers()
        self._go_to_search_the_transfer_market()
        self._set_bid_filter(name, price)

    def _go_to_transfers(self):
        go_to_transfers_button = Button(self.driver, selectors.GO_TO_TRANSFERS_BUTTON)
        go_to_transfers_button.safe_click()

    def _go_to_search_the_transfer_market(self):
        go_to_search_the_transfer_market_button = Button(self.driver, selectors.GO_TO_SEARCH_THE_TRANSFER_MARKET_BUTTON)
        go_to_search_the_transfer_market_button.safe_click()

    def _set_bid_filter(self, name, price):
        name_field = InputField(self.driver, selectors.NAME_FIELD)
        name_field.fill(name)

        name_button = Button(self.driver, selectors.NAME_BUTTON)
        name_button.slow_click()

        max_bid_price_field = InputField(self.driver, selectors.MAX_BID_PRICE_FIELD)
        max_bid_price_field.fill(price)

    def bid_on_items(self, price, max_items, max_time_left):
        self._search_the_transfer_market()
        self._bid_on_search_results(price, max_items, max_time_left)

    def _search_the_transfer_market(self):
        search_the_transfer_market_button = Button(self.driver, selectors.SEARCH_THE_TRANSFER_MARKET_BUTTON)
        search_the_transfer_market_button.slow_click()

    def _bid_on_search_results(self, price, max_items=20, max_time_left=60):
        number_of_items_bid_on = 0

        for item in self._get_search_results():
            random_pause(1)
            if number_of_items_bid_on >= max_items:
                break
            if self._get_time_left(item) >= max_time_left:
                break
            self._bid_on_item(item, price)
            number_of_items_bid_on = number_of_items_bid_on + 1

    def _get_search_results(self):
        search_results_list = List(self.driver, selectors.SEARCH_RESULTS_LIST)
        return search_results_list.get()

    def _get_time_left(self, item):
        player_item = Item(self.driver, item)
        return player_item.get_attribute(selectors.TIME_LEFT_LABEL)

    def _bid_on_item(self, item, price):
        player_item = Item(self.driver, item)
