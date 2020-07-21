class Login:
    def __init__(self, fut_web_app_service, logging_service):
        self.fut_web_app_service = fut_web_app_service
        self.logging_service = logging_service

    def execute(self, username, password):
        self.logging_service.log("Logging in to web app...")
        self.fut_web_app_service.login_service.go_to_login()
        self.fut_web_app_service.login_service.login(username, password)

        if self._security_code_required():
            self._enter_security_code()

        self.fut_web_app_service.login_service.wait_untill_loaded()

    def _security_code_required(self):
        return self.fut_web_app_service.login_service.security_code_required()

    def _enter_security_code(self):
        self.logging_service.log("Requesting security code...")
        self.fut_web_app_service.login_service.request_security_code()
        self.logging_service.log("Entering security code...")
        self.fut_web_app_service.login_service.enter_security_code(code=self._get_security_code())
        self.logging_service.log("Login succesful!")

    def _get_security_code(self):        
        return self.fut_web_app_service.verification_code_service.get()
