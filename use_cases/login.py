class Login:
    def __init__(self, login_service, verification_code_service):
        self._login_service = login_service
        self._verification_code_service = verification_code_service

    def execute(self, username, password):
        print("Logging in to web app...")
        self._login_service.go_to_login()
        self._login_service.login(username, password)

        if self._security_code_required():
            self._enter_security_code()

        self._login_service.wait_untill_loaded()

    def _security_code_required(self):
        return self._login_service.security_code_required()

    def _enter_security_code(self):
        print("Requesting security code...")
        self._login_service.request_security_code()
        print("Entering security code...")
        self._login_service.enter_security_code(code=self._get_security_code())
        print("Login succesful!")

    def _get_security_code(self):        
        return self._verification_code_service.get()
