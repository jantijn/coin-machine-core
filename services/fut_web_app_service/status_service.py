from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class StatusService:
    def __init__(self, driver):
        self.driver = driver

    def get_coins(self):
        return (
            WebDriverWait(self.driver, 30)
            .until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, "view-navbar-currency-coins")
                )
            )
            .text
        )

    def get_club_name(self):
        return (
            WebDriverWait(self.driver, 30)
            .until(
                EC.element_to_be_clickable((By.CLASS_NAME, "view-navbar-clubinfo-name"))
            )
            .text
        )
