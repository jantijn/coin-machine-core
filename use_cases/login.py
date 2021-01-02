from use_cases.exceptions.exceptions import WrongCredentialsException
from use_cases.responses import responses


class Login:
    def __init__(self, web_app, logger):
        self.web_app = web_app
        self.logger = logger

    def execute(self, username, password):
        self.logger.log("Logging in...")
        try:
            self.web_app.login.login(username, password)
        except WrongCredentialsException:
            msg = "Wrong username and or password"
            self.logger.log(msg)
            return responses.ResponseFailure.build_parameters_error(msg)

        self.logger.log("Login successful!")
        return responses.ResponseSuccess()
