from interfaces.web_app.selenium.exceptions import WrongCredentialsError


class Login:
    def __init__(self, web_app_interface, logger):
        self.web_app_interface = web_app_interface
        self.logger = logger

    def execute(self, username, password):
        self.logger.log('Logging in to web app')
        try:
            self.web_app_interface.login(username, password)
        except WrongCredentialsError:
            error_message = 'Wrong username and or password'
            self.logger.log(error_message)
            return {
                'success': False,
                'message': error_message
            }

        self.logger.log('Login successful!')
        return {
            'success': True,
            'message': 'Login successful!'
        }
