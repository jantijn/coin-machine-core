from use_cases.exceptions.exceptions import WrongVerificationCodeError
from use_cases.responses import responses


class VerifyDevice:
    def __init__(self, web_app, logger):
        self.web_app = web_app
        self.logger = logger

    def execute(self, verification_code):
        self.logger.log("Verifying device...")
        try:
            self.web_app.login.verify_device(verification_code)
        except WrongVerificationCodeError:
            msg = "Wrong verification code"
            self.logger.log(msg)
            return responses.ResponseFailure.build_parameters_error(msg)

        self.logger.log("Verify device successful!")
        return responses.ResponseSuccess()
