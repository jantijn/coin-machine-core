from interfaces.web_app.selenium import utils

VERIFICATION_CODE_FIELD = "#oneTimeCode"
CONFIRM_VERIFICATION_CODE_BUTTON = "#btnSubmit"
WRONG_VERIFICATION_CODE = "span.origin-ux-textbox-status-message.origin-ux-status-message"


def enter_verification_code(driver, verification_code):
    verification_code_field = utils.get_element(driver, VERIFICATION_CODE_FIELD)
    verification_code_field.safe_fill(verification_code)


def confirm_verification_code(driver):
    verification_code_button = utils.get_element(driver, CONFIRM_VERIFICATION_CODE_BUTTON)
    verification_code_button.slow_click()


def wrong_verification_code(driver):
    wrong_credentials_label = utils.get_element(driver, WRONG_VERIFICATION_CODE)
    return wrong_credentials_label.is_present()
