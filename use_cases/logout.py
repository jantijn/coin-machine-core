class Logout:
    def __init__(self, web_app, logger):
        self.web_app = web_app
        self.logger = logger

    def execute(self):
        self.logger.log("Logging out...")
        self.web_app.logout()
