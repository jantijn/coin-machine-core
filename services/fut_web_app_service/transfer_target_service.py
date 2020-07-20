from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from services.fut_web_app_service.helpers import safe_fill

CLEAR_EXPIRED_BUTTON = "/html/body/main/section/section/div[2]/div/div/div/section[4]/header/button"
LIST_BUTTON = "/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[1]/button"
START_PRICE_FIELD = "/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/input"
MAX_BUY_NOW_FIELD = "/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[2]/div[3]/div[2]/input"
CONFIRM_LIST_BUTTON = "/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[2]/button"

class TransferTargetService:
    def __init__(self, driver):
        self.driver = driver

    def clear_expired_players(self):
        try:
            WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, CLEAR_EXPIRED_BUTTON))
            ).click()
        except TimeoutException:
            return False
        return True

    def list_all_won_items(self, price):
        number_of_won_players = len(self.get_won_items())
        for i in range(1, number_of_won_players):
            item = self.get_won_items()[0]
            print('item')
            time.sleep(1)
            item.click()
            time.sleep(1)
            self.list_on_transfer_market()
            self.set_start_price(price -100)
            self.set_max_buy_now_price(price)
            self.list_item()

    def get_won_items(self):
        return self.driver.find_elements_by_class_name('won')

    def get_item_name(self, item):
        return item.find_elements_by_class_name('name')[0].text

    def select(self, item):
        item.click()
        return item

    def list_on_transfer_market(self):
        time.sleep(1)
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "accordian"))
        ).click()
        time.sleep(1)

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
            EC.element_to_be_clickable((By.XPATH, CONFIRM_LIST_BUTTON))
        ).click()
        time.sleep(1)
