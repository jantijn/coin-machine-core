import random
import time

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class NavigationService:
    def __init__(self, driver):
        self.driver = driver

    def go_to_transfers(self):
        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "showing"))
        )

        try:
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "icon-transfer"))
            ).click()
        except ElementClickInterceptedException:
            self.go_to_transfers()

    def go_to_search_the_transfer_market(self):
        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "showing"))
        )

        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "tileContent"))
        ).click()

    def go_to_transfer_list(self):
        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "showing"))
        )

        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "ut-tile-transfer-list"))
        ).click()

    def go_to_transfer_targets(self):
        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "showing"))
        )

        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "ut-tile-transfer-targets"))
        ).click()

    def go_back(self):
        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "showing"))
        )

        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "ut-navigation-button-control"))
        ).click()

    def get_location(self):
        return (
            WebDriverWait(self.driver, 30)
            .until(EC.element_to_be_clickable((By.CLASS_NAME, "title")))
            .text
        )

    def go_to_settings(self):
        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "showing"))
        )

        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "icon-settings"))
        ).click()

    def refresh(self):
        self.driver.refresh()

    def prove_you_are_not_a_robot(self):
        try:
            return (
                WebDriverWait(self.driver, 5)
                .until(EC.element_to_be_clickable((By.CLASS_NAME, "dialog-title")))
                .text
                == "Verification Required"
            )
        except TimeoutException:
            return False
