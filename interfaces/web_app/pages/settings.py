from interfaces.web_app.pages import utils

LOGOUT_BUTTON = "body > main > section > section > div.ut-navigation-container-view--content > div > div > div.ut-app-settings-actions > div:nth-child(1) > button:nth-child(4)"
CONFIRM_LOGOUT_BUTTON = "body > div.view-modal-container.form-modal > section > div > div > button:nth-child(1)"


def logout(driver):
    logout_button = utils.get_element(driver, LOGOUT_BUTTON)
    logout_button.slow_click()


def confirm_logout(driver):
    confirm_logout_button = utils.get_element(driver, CONFIRM_LOGOUT_BUTTON)
    confirm_logout_button.slow_click()
