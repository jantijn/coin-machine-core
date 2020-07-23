import random
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


class Button:
    def __init__(self, driver, selector):
        self.driver = driver
        self.selector = selector
        if self.is_present():
            self.button = self.driver.find_element_by_css_selector(selector)

    def is_present(self):
        return _is_present(self.driver, self.selector)

    def fast_click(self):
        time.sleep(random.randint(0, 10) / 100)
        self._click()

    def slow_click(self):
        time.sleep(random.randint(0, 100) / 100)
        self._click()

    def _click(self):
        [height, width] = self._get_button_dimensions()
        [height_rand, width_rand] = _create_random_offset(height, width)
        action = ActionChains(self.driver)
        action.move_to_element_with_offset(self.button, width_rand, height_rand)
        action.click()
        action.perform()

    def _get_button_dimensions(self):
        size = self.button.size
        size_list = list(size.values())
        height = int(size_list[0]) - 1
        width = int(size_list[1]) - 1
        return [height, width]


class InputField:
    def __init__(self, driver, selector):
        self.driver = driver
        self.selector = selector
        if self.is_present():
            self.button = self.driver.find_element_by_css_selector(selector)

    def is_present(self):
        return _is_present(self.driver, self.selector)

    def fill(self, text):
        while self.field.get_attribute("value") != text:
            self.field.clear()
            for char in text:
                time.sleep(random.randint(0, 10) / 100)
                self.field.send_keys(char)


class Notification:
    def __init__(self, driver, selector):
        self.driver = driver
        self.selector = selector

    def is_present(self):
        return _is_present(self.driver, self.selector)


def _is_present(driver, selector):
    timeout = 5
    try:
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
        )
    except TimeoutException:
        return False
    return True


def _create_random_offset(height, width):
    try:
        height_rand = random.randint(1, height)
    except ValueError:
        height_rand = 1
    try:
        width_rand = random.randint(1, width)
    except ValueError:
        width_rand = 1
    return [height_rand, width_rand]