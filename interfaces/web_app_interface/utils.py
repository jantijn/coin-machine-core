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
        self.button = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
        )
        [self.height, self.width] = self._get_button_dimensions()

    def fast_click(self):
        time.sleep(random.randint(0, 10) / 100)
        self._click()

    def slow_click(self):
        time.sleep(random.randint(0, 100) / 100)
        self._click()

    def _click(self):
        [height_rand, width_rand] = self._create_random_offset()
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

    def _create_random_offset(self):
        try:
            height_rand = random.randint(1, self.height)
        except ValueError:
            height_rand = 1
        try:
            width_rand = random.randint(1, self.width)
        except ValueError:
            width_rand = 1
        return [height_rand, width_rand]


class InputField:
    def __init__(self, driver, selector):
        self.driver = driver
        self.field = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
        )

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
        try:
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.selector))
            )
        except TimeoutException:
            return False
        return True
