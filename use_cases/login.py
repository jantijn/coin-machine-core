class Login:
    def __init__(self, fut_web_app_service, logging_service):
        self.fut_web_app_service = fut_web_app_service
        self.logging_service = logging_service

    def execute(self, username, password):
        self._login(username, password)

        if self._login_failed():
            self.logging_service.log("Wrong credentials provided")
            return False

        if self._security_code_required():
            self._request_security_code()

        self.fut_web_app_service.login_service.wait_untill_loaded()
        return True

    def _login(self, username, password):
        self.logging_service.log("Logging in to web app")
        self.fut_web_app_service.login_service.go_to_login()
        self.fut_web_app_service.login_service.login(username, password)

    def _login_failed(self):
        return self.fut_web_app_service.login_service.login_failed()

    def _security_code_required(self):
        return self.fut_web_app_service.login_service.security_code_required()

    def _request_security_code(self):
        self.logging_service.log("Requesting security code")
        self.fut_web_app_service.login_service.request_security_code()
