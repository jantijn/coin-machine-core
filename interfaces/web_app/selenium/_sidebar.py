from interfaces.web_app.selenium import utils

GO_TO_TRANSFERS_BUTTON = "button.ut-tab-bar-item.icon-transfer"


def go_to_transfers(driver):
    go_to_transfers_button = utils.get_element(driver, GO_TO_TRANSFERS_BUTTON)
    go_to_transfers_button.safe_click()
