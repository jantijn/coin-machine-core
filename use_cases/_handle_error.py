class HandleError:
    def __init__(self, web_app, logger):
        self.web_app = web_app
        self.logger = logger

    def execute(self):
        self._restart_web_app()

    def _restart_web_app(self):
        self.logger.log("Something went wrong, restarting the web app...")
        self.web_app.refresh()
