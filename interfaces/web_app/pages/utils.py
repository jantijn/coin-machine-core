import random
import time

from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    NoSuchElementException,
    MoveTargetOutOfBoundsException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver import ActionChains


class WebAppElement:
    def __init__(self, driver, selenium_element):
        self.driver = driver
        self.selenium_element = selenium_element

    @classmethod
    def from_selector(cls, driver, selector, timeout):
        try:
            selenium_element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
        except TimeoutException:
            selenium_element = None
        return cls(driver=driver, selenium_element=selenium_element)

    def is_present(self):
        return bool(self.selenium_element)

    def get_text(self):
        return self.selenium_element.text

    def get_attribute(self, selector):
        try:
            return self.selenium_element.find_element_by_css_selector(selector).text
        except (NoSuchElementException, StaleElementReferenceException):
            return ""

    def get_classes(self):
        try:
            return self.selenium_element.get_attribute("class").split()
        except (NoSuchElementException, StaleElementReferenceException):
            return []

    def fast_click(self):
        time.sleep(random.randint(0, 10) / 1000)
        self._click()

    def slow_click(self):
        time.sleep(random.randint(0, 100) / 100)
        self._click()

    def safe_click(self):
        time.sleep(random.randint(0, 500) / 100)
        try:
            self._click()
        except ElementClickInterceptedException:
            self.safe_click()

    def _click(self):
        [height, width] = self._get_web_app_object_dimensions(self.selenium_element)
        [height_rand, width_rand] = self._create_random_offset(height, width)
        action = ActionChains(self.driver)
        try:
            action.move_to_element_with_offset(
                self.selenium_element, width_rand, height_rand
            )
            action.click()
            action.perform()
        except MoveTargetOutOfBoundsException:
            self._click()
        except StaleElementReferenceException:
            pass

    @staticmethod
    def _get_web_app_object_dimensions(web_app_object):
        size = web_app_object.size
        size_list = list(size.values())
        height = int(size_list[0]) - 1
        width = int(size_list[1]) - 1
        return [height, width]

    @staticmethod
    def _create_random_offset(height, width):
        middle_height = int(height / 2)
        middle_width = int(width / 2)
        height_rand = random.randint(middle_height - 2, middle_height + 2)
        width_rand = random.randint(middle_width - 2, middle_width + 2)
        return [height_rand, width_rand]

    def safe_fill(self, text):
        text = str(text)
        while self.selenium_element.get_attribute("value") != text:
            self.selenium_element.clear()
            self.slow_click()
            for char in text:
                time.sleep(random.randint(0, 10) / 100)
                self.selenium_element.send_keys(char)

    def fast_fill(self, text):
        text = str(text)
        while self.selenium_element.get_attribute("value") != text:
            self.selenium_element.clear()
            self.slow_click()
            for char in text:
                time.sleep(random.randint(0, 10) / 1000)
                self.selenium_element.send_keys(char)


def element_exists(driver, selector):
    timeout = 2
    try:
        web_app_object = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
        )
    except TimeoutException:
        web_app_object = None
    return bool(web_app_object)


def get_element(driver, selector, timeout=15):
    element = WebAppElement.from_selector(driver, selector, timeout)
    return element


def get_elements(driver, selector, class_=None):
    elements = driver.find_elements_by_css_selector(selector)
    if class_:
        return [class_(driver, element) for element in elements]
    else:
        return [WebAppElement(driver, element) for element in elements]
