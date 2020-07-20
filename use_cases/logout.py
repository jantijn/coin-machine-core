class Logout:
    def __init__(self, log_out_service, navigation_service):
        self._log_out_service = log_out_service
        self._navigation_service = navigation_service

    def execute(self):
        self._navigation_service.go_to_settings()
        self._log_out_service.log_out()
        self._log_out_service.confirm_log_out()
