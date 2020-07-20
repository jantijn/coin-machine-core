class HandleError:
    def __init__(self, fut_web_app_service, logging_service):
        self.fut_web_app_service = fut_web_app_service
        self._logging_service = logging_service

    def execute(self):
        self._logging_service.log("Something went wrong...")

        # if self.fut_web_app_service.navigation_service.prove_you_are_not_a_robot():
        #     self._logging_service.log("Please log into web app and do Captcha exercise")

        self._logging_service.log("Restarting the app")
        self.fut_web_app_service.navigation_service.refresh()
