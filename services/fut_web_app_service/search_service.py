from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from services.fut_web_app_service.helpers import safe_fill

NAME_FIELD = "/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[1]/div[1]/div/input"
NAME_DROPDOWN = "/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[1]/div[1]/div/div/ul/button[1]"
MAX_BUY_NOW_FIELD = "/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[2]/div[6]/div[2]/input"
MAX_BID_FIELD = "/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[2]/div[3]/div[2]/input"
MIN_BID_FIELD = "/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[2]/input"


class SearchService:
    def __init__(self, driver):
        self.driver = driver

    def set_player_name(self, player_name):
        element = self.driver.find_element_by_xpath(NAME_FIELD)
        safe_fill(element, player_name)

        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, NAME_DROPDOWN))
        ).click()

    def set_max_buy_now_price(self, price):
        element = self.driver.find_element_by_xpath(MAX_BUY_NOW_FIELD)
        safe_fill(element, str(price))

    def set_max_bid_price(self, price):
        element = self.driver.find_element_by_xpath(MAX_BID_FIELD)
        safe_fill(element, str(price))

    def set_min_bid_price(self, price):
        element = self.driver.find_element_by_xpath(MIN_BID_FIELD)
        safe_fill(element, str(price))

    def get_min_bid_price(self):
        min_bid_price = self.driver.find_element_by_xpath(MIN_BID_FIELD).get_attribute(
            "value"
        )
        if min_bid_price == "":
            return 0
        else:
            return int(min_bid_price)

    def search(self):
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "call-to-action"))
        ).click()

    def reset_search(self):
        min_bid_price = self.get_min_bid_price()
        if min_bid_price >= 600:
            self.set_min_bid_price(150)
        else:
            self.set_min_bid_price(min_bid_price + 150)
