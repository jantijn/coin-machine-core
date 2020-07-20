class RefreshTransferList:
    def __init__(self, transfer_list_service, navigation_service, logging_service):
        self._transfer_list_service = transfer_list_service
        self._navigation_service = navigation_service
        self._logging_service = logging_service

    def execute(self):
        self._go_to_transfer_list()
        self._refresh_transfer_list()

    def _go_to_transfer_list(self):
        self._logging_service.log("")
        self._logging_service.log("-" * 80)
        self._logging_service.log("Going to the transfer list...")
        self._navigation_service.go_to_transfers()
        self._navigation_service.go_to_transfer_list()

    def _refresh_transfer_list(self):
        self._logging_service.log("Refreshing the transfer list...")
        self._transfer_list_service.remove_sold_players()
        self._transfer_list_service.relist_unsold_players()
        self._transfer_list_service.confirm_relist()
        self._logging_service.log("Transfer list refreshed!")
