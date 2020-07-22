from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from factories.web_driver_factory import build_web_driver


class Button:
    def __init__(self, driver, selector):
        self.driver = driver
        self.field = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(By.CSS_SELECTOR, selector)
        )

    def click(self):
        self.field.click()

class TextField:
    def __init__(self, driver, selector):
        self.driver = driver
        self.field = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(By.CSS_SELECTOR, selector)
        )

    def fill(self, text):
        while self.field.get_attribute("value") != text:
            self.field.clear()
            self.field.send_keys(text)


class FutService:
    def __init__(self, driver):
        self.driver = driver

    def login(self, email, password):
        self._go_to_login()
        # self._enter_credentials(email, password)
        # self._confirm.credentials()

    def _go_to_login(self):
        SELECTOR = 'button.btn-standard.call-to-action'
        button = Button(self.driver, SELECTOR)
        button.click()

    # def _enter_credentials(self, email, password):
    #     element = self.driver.find_element_by_id("email")
    #     element.clear()
    #     element.send_keys(email)
    #     self.driver.find_element_by_id("password").send_keys(password)
    #
    # def _confirm_credentials(self):
    #     WebDriverWait(self.driver, 30).until(
    #         EC.element_to_be_clickable((By.ID, "btnLogin"))
    #     ).click()


if __name__ == "__main__":
    driver = build_web_driver(headless = False)
    fut_service = FutService(driver)
    fut_service._go_to_login()
