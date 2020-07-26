from use_cases.exceptions.exceptions import WrongVerificationCodeError


class VerifyDevice:
    def __init__(self, web_app_interface, logger):
        self.web_app_interface = web_app_interface
        self.logger = logger

    def execute(self, verification_code):
        self.logger.log('Logging in to web app')
        try:
            self.web_app_interface.verify_device(verification_code)
        except WrongVerificationCodeError:
            error_message = 'Wrong verification code'
            self.logger.log(error_message)
            return {
                'success': False,
                'message': error_message
            }
        success_message = 'Verify device successful'
        self.logger.log(success_message)
        return {
            'success': True,
            'message': success_message
        }