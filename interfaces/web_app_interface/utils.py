import random
import time

from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    NoSuchElementException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

from interfaces.web_app_interface import selectors


class WebAppObject:
    def __init__(self, driver, web_app_object):
        self.driver = driver
        self.web_app_object = web_app_object

    @classmethod
    def from_selector(cls, driver, selector):
        timeout = 5
        try:
            web_app_object = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
        except TimeoutException:
            web_app_object = None
        return cls(driver=driver, web_app_object=web_app_object)

    def is_present(self):
        return bool(self.web_app_object)


class ClickableWebAppObject(WebAppObject):
    def fast_click(self):
        time.sleep(random.randint(0, 10) / 100)
        self._click()

    def slow_click(self):
        time.sleep(random.randint(0, 100) / 100)
        self._click()

    def safe_click(self):
        time.sleep(random.randint(0, 100) / 100)
        try:
            self._click()
        except ElementClickInterceptedException:
            self.safe_click()

    def _click(self):
        [height, width] = self._get_web_app_object_dimensions(self.web_app_object)
        [height_rand, width_rand] = self._create_random_offset(height, width)
        action = ActionChains(self.driver)
        action.move_to_element_with_offset(self.web_app_object, width_rand, height_rand)
        action.click()
        action.perform()

    @staticmethod
    def _get_web_app_object_dimensions(web_app_object):
        size = web_app_object.size
        size_list = list(size.values())
        height = int(size_list[0]) - 1
        width = int(size_list[1]) - 1
        return [height, width]

    @staticmethod
    def _create_random_offset(height, width):
        height_rand = random.randint(1, height)
        width_rand = random.randint(1, width)
        return [height_rand, width_rand]


class ItemList:
    def __init__(self, driver, item_list):
        self.driver = driver
        self.item_list = []
        for item in item_list:
            self.item_list.append(Item(driver, item))

    @classmethod
    def from_selector(cls, driver, selector):
        timeout = 5
        try:
            item_list = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        except TimeoutException:
            item_list = []
        return cls(driver=driver, item_list=item_list)

    def get_items(self):
        return self.item_list


class Item(ClickableWebAppObject):
    def get_time_left(self):
        time_left_string = self._get_attribute_by_selector(selectors.TIME_LEFT_LABEL)
        return self._convert_time_left_string_to_number(time_left_string)

    def _get_attribute_by_selector(self, selector):
        try:
            return self.web_app_object.find_element_by_css_selector(selector).text
        except NoSuchElementException:
            return ""

    @staticmethod
    def _convert_time_left_string_to_number(time_left_string):
        number = time_left_string.split(" ")[0].replace("<", "")
        unit = time_left_string.split(" ")[1]
        if unit == "Seconds":
            return 1
        elif unit == "Hours" or unit == "Hour":
            return 60
        return int(number)

    def bid(self, price):
        self.slow_click()
        self._set_bid_price(price)
        self._bid()

    def _set_bid_price(self, price):
        bid_price_field = InputField.from_selector(self.driver, selectors.BID_PRICE_FIELD)
        bid_price_field.fill(price)

    def _bid(self):
        bid_button = Button.from_selector(self.driver, selectors.BID_BUTTON)
        bid_button.slow_click()


class Button(ClickableWebAppObject):
    pass


class InputField(WebAppObject):
    def fill(self, text):
        while self.web_app_object.get_attribute("value") != text:
            self.web_app_object.clear()
            for char in text:
                time.sleep(random.randint(0, 10) / 100)
                self.web_app_object.send_keys(char)


class Label(WebAppObject):
    pass
