from selenium.webdriver.common.by import By
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

class BidService:
    def __init__(self, driver):
        self.driver = driver

    def get_search_results(self):
        return self.driver.find_elements_by_class_name('listFUTItem')

    def select(self, item):
        item.click()
        return item

    def get_time_left(self, item):
        time_left_string = item.find_elements_by_class_name('time')[0].text
        number = time_left_string.split(' ')[0].replace('<', '')
        unit = time_left_string.split(' ')[1]
        if unit == 'Seconds':
            return 1
        elif unit == 'Hours' or unit == 'Hour':
            return 60
        return int(number)

    def set_bid_price(self, price):
        element = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, BID_FIELD))
        )
        safe_fill(element, str(price), manual_reset=True)

    def bid(self):
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "bidButton"))
        ).click()
        time.sleep(0.5)
