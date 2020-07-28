class RefreshTransferList:
    def __init__(self, web_app, logger):
        self.web_app = web_app
        self.logger = logger

    def execute(self):
        self.logger.log("Refreshing the transfer list...")
        self.web_app.refresh_transfer_list()
        self.logger.log("Transfer list refreshed")
