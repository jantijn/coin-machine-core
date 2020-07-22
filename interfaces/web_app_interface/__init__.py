from interfaces.web_app_interface.exceptions import WrongCredentialsError
from interfaces.web_app_interface.login_page import LoginPage


class WebAppInterface:
    
    def __init__(self, driver):
        self.driver = driver

    def login(self, email, password):
        lp = LoginPage(self.driver)

        lp.go_to_login()
        lp.enter_credentials(email, password)
        lp.confirm_credentials()
        if lp.wrong_credentials():
            raise WrongCredentialsError('Wrong email address or password')
