import time

from services.fut_web_app_service.helpers import safe_fill

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginService:
    def __init__(self, driver):
        self.driver = driver

    def go_to_login(self):
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn-standard"))
        ).click()

    def login(self, username, password):
        button = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.ID, "btnLogin"))
        )

        element = self.driver.find_element_by_id("email")
        element.clear()
        element.send_keys(username)

        self.driver.find_element_by_id("password").send_keys(password)
        button.click()

    def request_security_code(self):
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.ID, "btnSendCode"))
        ).click()

    def enter_security_code(self, code):
        button = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.ID, "btnSubmit"))
        )
        self.driver.find_element_by_id("oneTimeCode").send_keys(code)
        button.click()

    def wait_untill_loaded(self):
        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "ut-click-shield"))
        )
        time.sleep(10)

    def security_code_required(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "twoStepHeader"))
            ).click()
        except TimeoutException:
            return False
        return True
