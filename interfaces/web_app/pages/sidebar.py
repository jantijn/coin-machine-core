from interfaces.web_app.pages import utils

GO_TO_TRANSFERS_BUTTON = "button.ut-tab-bar-item.icon-transfer"
GO_TO_SETTINGS_BUTTON = "button.ut-tab-bar-item.icon-settings"
LOCATION_LABEL = "h1.title"


def go_to_transfers(driver):
    go_to_transfers_button = utils.get_element(driver, GO_TO_TRANSFERS_BUTTON)
    go_to_transfers_button.safe_click()


def go_to_settings(driver):
    go_to_settings_button = utils.get_element(driver, GO_TO_SETTINGS_BUTTON)
    go_to_settings_button.safe_click()


def get_location(driver):
    location_label = utils.get_element(driver, LOCATION_LABEL)
    return location_label.get_text()
