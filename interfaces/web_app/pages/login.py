from interfaces.web_app.pages import utils

GO_TO_LOGIN_BUTTON = "#Login > div > div > button.btn-standard.call-to-action"
CREDENTIALS = "div.login-form-container"
EMAIL_FIELD = "#email"
PASSWORD_FIELD = "#password"
CONFIRM_CREDENTIALS_BUTTON = "#btnLogin"
WRONG_CREDENTIALS_LABEL = "#loginForm > div.general-error > div > div"
REQUEST_CODE_BUTTON = "#btnSendCode"


def login_required(driver):
    return utils.element_exists(driver, GO_TO_LOGIN_BUTTON)


def go_to_login(driver):
    go_to_login_button = utils.get_element(driver, GO_TO_LOGIN_BUTTON)
    go_to_login_button.slow_click()


def credentials_required(driver):
    return utils.element_exists(driver, CREDENTIALS)


def enter_credentials(driver, email, password):
    email_field = utils.get_element(driver, EMAIL_FIELD)
    email_field.safe_fill(email)

    password_field = utils.get_element(driver, PASSWORD_FIELD)
    password_field.safe_fill(password)


def confirm_credentials(driver):
    confirm_credentials_button = utils.get_element(driver, CONFIRM_CREDENTIALS_BUTTON)
    confirm_credentials_button.slow_click()


def wrong_credentials(driver):
    return utils.element_exists(driver, WRONG_CREDENTIALS_LABEL)


def verification_code_required(driver):
    return utils.element_exists(driver, REQUEST_CODE_BUTTON)


def request_verification_code(driver):
    request_code_button = utils.get_element(driver, REQUEST_CODE_BUTTON)
    request_code_button.slow_click()
