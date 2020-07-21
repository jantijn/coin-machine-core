class RefreshTransferList:
    def __init__(self, fut_web_app_service, logging_service):
        self.fut_web_app_service = fut_web_app_service
        self.logging_service = logging_service

    def execute(self):
        self._go_to_transfer_list()
        self._refresh_transfer_list()

    def _go_to_transfer_list(self):
        self.logging_service.log("Going to the transfer list")
        self.fut_web_app_service.navigation_service.go_to_transfers()
        self.fut_web_app_service.navigation_service.go_to_transfer_list()

    def _refresh_transfer_list(self):
        self.logging_service.log("Refreshing the transfer list")
        self.fut_web_app_service.transfer_list_service.remove_sold_players()
        self.fut_web_app_service.transfer_list_service.relist_unsold_players()
        self.fut_web_app_service.transfer_list_service.confirm_relist()
        self.logging_service.log("Transfer list refreshed!")
