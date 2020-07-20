from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

REMOVE_SOLD_PLAYERS_BUTTON = (
    "/html/body/main/section/section/div[2]/div/div/div/section[1]/header/button"
)
RELIST_UNSOLD_PLAYERS_BUTTON = (
    "/html/body/main/section/section/div[2]/div/div/div/section[2]/header/button"
)
CONFIRM_RELIST_BUTTON = "/html/body/div[4]/section/div/div/button[2]"


class TransferListService:
    def __init__(self, driver):
        self.driver = driver

    def remove_sold_players(self):
        try:
            WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, REMOVE_SOLD_PLAYERS_BUTTON))
            ).click()
        except TimeoutException:
            return False
        return True

    def relist_unsold_players(self):
        try:
            WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, RELIST_UNSOLD_PLAYERS_BUTTON))
            ).click()
        except TimeoutException:
            return False
        return True

    def confirm_relist(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, CONFIRM_RELIST_BUTTON))
            ).click()
        except TimeoutException:
            return False
        return True
