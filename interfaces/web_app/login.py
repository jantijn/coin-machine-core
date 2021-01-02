from interfaces.web_app.pages import login, verify_device, general, home
from use_cases.exceptions.exceptions import (
    WrongCredentialsException,
    WrongVerificationCodeError,
)


class Login:
    def __init__(self, driver):
        self.driver = driver

    def login_required(self):
        return login.login_required(self.driver)

    def login(self, email=None, password=None):
        login.go_to_login(self.driver)
        if login.credentials_required(self.driver):
            self._enter_credentials(email, password)
        else:
            self._clear_home_screen()

    def _enter_credentials(self, email, password):
        login.enter_credentials(self.driver, email, password)
        login.confirm_credentials(self.driver)
        if login.wrong_credentials(self.driver):
            raise WrongCredentialsException("Wrong email address or password")
        if login.verification_code_required(self.driver):
            login.request_verification_code(self.driver)
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
