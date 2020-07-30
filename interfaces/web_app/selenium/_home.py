from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from interfaces.web_app.selenium import utils

POP_UP_BUTTON = "div.ut-livemessage-footer > button"


def wait_until_loaded(driver):
    WebDriverWait(driver, 60).until(EC.invisibility_of_element_located((By.CLASS_NAME, "ut-click-shield")))


def handle_pop_ups(driver):
    pop_up_button = utils.get_element(driver, POP_UP_BUTTON)
    while pop_up_button.is_present():
        pop_up_button.slow_click()
        pop_up_button = utils.get_element(driver, POP_UP_BUTTON)
