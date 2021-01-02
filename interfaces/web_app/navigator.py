from interfaces.web_app.pages import sidebar, transfers


class Navigator:
    def __init__(self, driver):
        self.driver = driver

    def go_to_search_the_transfer_market(self):
        sidebar.go_to_transfers(self.driver)
        transfers.go_to_search_the_transfer_market(self.driver)

    def go_to_transfer_targets(self):
        sidebar.go_to_transfers(self.driver)
        transfers.go_to_transfer_targets(self.driver)

    def go_to_transfer_list(self):
        sidebar.go_to_transfers(self.driver)
        transfers.go_to_transfer_list(self.driver)
