class HandleError:
    def __init__(self, web_app, logger):
        self.web_app = web_app
        self.logger = logger

    def execute(self, e=None):
        self.logger.log("Something went wrong, restarting the web app...")
        self._restart_web_app()

    def _restart_web_app(self):
        self.web_app.login.refresh()
        if self.web_app.login.login_required():
            self.logger.log("Logging in...")
            self.web_app.login.login()
