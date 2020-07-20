from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from services.fut_web_app_service.helpers import safe_fill

import time


START_PRICE_FIELD = (
    "/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div[2]/div["
    "2]/div[2]/input "
)
MAX_BUY_NOW_FIELD = (
    "/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div[2]/div["
    "3]/div[2]/input "
)
BID_FIELD = "/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div/input"

class PurchaseService:
    def __init__(self, driver):
        self.driver = driver

    def buy_now(self):
        try:
            WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "buyButton"))
            ).click()
        except TimeoutException:
            return False
        except ElementClickInterceptedException:
            self.buy_now()
        except StaleElementReferenceException:
            self.buy_now()
        return True

    def confirm_buy_now(self):
        try:
            WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/ html / body / div[4] / section / div / div / button[1]",
                    )
                )
            ).click()
        except TimeoutException:
            return False
        return True

    def outbit_by_other_player(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "Notification"))
            ).click()
            WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "icon_close"))
            ).click()
        except TimeoutException:
            return False
        return True

    def list_on_transfer_market(self):
        time.sleep(1)
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "accordian"))
        ).click()
        time.sleep(1)

    def set_bid_price(self, price):
        element = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, BID_FIELD))
        )
        safe_fill(element, str(price), manual_reset=True)

    def set_start_price(self, price):
        element = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, START_PRICE_FIELD))
        )
        safe_fill(element, str(price), manual_reset=True)

    def set_max_buy_now_price(self, price):
        element = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, MAX_BUY_NOW_FIELD))
        )
        safe_fill(element, str(price), manual_reset=True)

    def list_item(self):
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "call-to-action"))
        ).click()
        time.sleep(1)

    def get_purchase_price(self):
        return int(
            self.driver.find_elements_by_class_name("boughtPriceValue")[0].text.replace(
                ",", ""
            )
        )

    def bid_on_all_search_results(self, price):
        for item in self.get_search_results():
            time.sleep(1)
            item.click()
            time.sleep(1)
            self.set_bid_price(price)
            self.bid()

    def get_search_results(self):
        return self.driver.find_elements_by_class_name('listFUTItem')

    def bid(self):
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "bidButton"))
        ).click()
        time.sleep(0.5)
