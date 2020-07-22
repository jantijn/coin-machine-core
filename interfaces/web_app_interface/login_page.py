from interfaces.web_app_interface.utils import Button, InputField, Notification

GO_TO_LOGIN_BUTTON = 'button.btn-standard.call-to-action'
EMAIL_FIELD = '#email'
PASSWORD_FIELD = '#password'
CONFIRM_CREDENTIALS_BUTTON = '#btnLogin'
WRONG_CREDENTIALS_NOTIFICATION = '#loginForm > div.general-error > div > div'


class LoginPage():

    def __init__(self, driver):
        self.driver = driver

    def go_to_login(self):
        go_to_login_button = Button(self.driver, GO_TO_LOGIN_BUTTON)
        go_to_login_button.slow_click()

    def enter_credentials(self, email, password):
        email_field = InputField(self.driver, EMAIL_FIELD)
        email_field.fill(email)

        password_field = InputField(self.driver, PASSWORD_FIELD)
        password_field.fill(password)

    def confirm_credentials(self):
        confirm_credentials_button = Button(self.driver, CONFIRM_CREDENTIALS_BUTTON)
        confirm_credentials_button.slow_click()

    def wrong_credentials(self):
        wrong_credentials_notification = Notification(self.driver, WRONG_CREDENTIALS_NOTIFICATION)
        return wrong_credentials_notification.is_present()
