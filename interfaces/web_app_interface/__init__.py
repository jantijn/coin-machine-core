from interfaces.web_app_interface import selectors
from interfaces.web_app_interface.exceptions import WrongCredentialsError, WrongVerificationCodeError
from interfaces.web_app_interface.utils import Button, InputField, Notification


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

    def verify_device(self, verification_code):
        self._enter_verification_code(verification_code)
        self._confirm_verification_code()
        if self._wrong_verification_code
            raise WrongVerificationCodeError('Wrong verification code')

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
        wrong_credentials_notification = Notification(self.driver, selectors.WRONG_CREDENTIALS_NOTIFICATION)
        return wrong_credentials_notification.is_present()

    def _verification_code_required(self):

