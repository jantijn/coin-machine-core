class EnterVerificationCode:
    def __init__(self, fut_web_app_service, logging_service):
        self.fut_web_app_service = fut_web_app_service
        self.logging_service = logging_service

    def execute(self, verification_code):
        self.logging_service.log('Entering security code')
        self.fut_web_app_service.login_service.enter_security_code(code=verification_code)

        if self.fut_web_app_service.login_service.wrong_verification_code():
            self.logging_service.log('Wrong verification code entered')
            return False

        self.fut_web_app_service.login_service.wait_untill_loaded()
        self.logging_service.log('Successfully logged into the webapp')
        return True
