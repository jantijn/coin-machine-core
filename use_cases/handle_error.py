class HandleError:
    def __init__(self, navigation_service, logging_service):
        self._navigation_service = navigation_service
        self._logging_service = logging_service

    def execute(self):
        self._logging_service.log("-" * 80)
        self._logging_service.log("Something went wrong...")

        if self._navigation_service.prove_you_are_not_a_robot():
            self._logging_service.log("Please log into web app and do Captcha exercise")
            input("Press enter to continue")

        self._navigation_service.refresh()
