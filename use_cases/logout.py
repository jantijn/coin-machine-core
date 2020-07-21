class Logout:
    def __init__(self, fut_web_app_service, logging_service):
        self.fut_web_app_service.log_out_service = fut_web_app_service
        self.logging_service = logging_service

    def execute(self):
        self.logging_service.log('Logging out')
        self.fut_web_app_service.navigation_service.go_to_settings()
        self.fut_web_app_service.log_out_service.log_out()
        self.fut_web_app_service.log_out_service.confirm_log_out()
        self.logging_service.log('Logged out')
