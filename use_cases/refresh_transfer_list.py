from use_cases.handle_error import HandleError


class RefreshTransferList:
    def __init__(self, web_app, logger):
        self.web_app = web_app
        self.logger = logger

    def execute(self):
        self.logger.log("Refreshing the transfer list...")
        self._refresh_transfer_list()
        self.logger.log("Transfer list refreshed")

    def _refresh_transfer_list(self):
        try:
            self.web_app.refresh_transfer_list()
        except:
            self._handle_error()
            self._refresh_transfer_list()

    def _handle_error(self):
        handle_error = HandleError(web_app=self.web_app, logger=self.logger)
        handle_error.execute()
