from use_cases.exceptions.exceptions import WrongCredentialsError


class Login:
    def __init__(self, web_app, logger):
        self.web_app = web_app
        self.logger = logger

    def execute(self, username, password):
        self.logger.log('Logging in to web app')
        try:
            self.web_app.login(username, password)
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
