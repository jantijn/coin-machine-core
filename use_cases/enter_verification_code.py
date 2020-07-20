class EnterVerificationCode:
    def __init__(self, login_service):
        self._login_service = login_service

    def execute(self, verification_code):
        self._login_service.enter_security_code(code=verification_code)

        self._login_service.wait_untill_loaded()
