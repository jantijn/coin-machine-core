from use_cases.exceptions.exceptions import WrongVerificationCodeError
from use_cases.responses import responses


class VerifyDevice:
    def __init__(self, web_app_interface, logger):
        self.web_app_interface = web_app_interface
        self.logger = logger

    def execute(self, verification_code):
        self.logger.log("Logging in to web app")
        try:
            self.web_app_interface.verify_device(verification_code)
        except WrongVerificationCodeError:
            msg = "Wrong verification code"
            self.logger.log(msg)
            return responses.ResponseFailure.build_parameters_error(msg)
        except Exception as exc:
            self.logger.log("Something went wrong")
            return responses.ResponseFailure.build_system_error(exc)

        self.logger.log("Verify device successful!")
        return responses.ResponseSuccess()
