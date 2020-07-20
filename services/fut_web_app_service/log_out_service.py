from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SIGN_OUT_BUTTON = (
    "/html/body/main/section/section/div[2]/div/div/div[2]/div[1]/button[3]"
)
CONFIRM_SIGN_OUT_BUTTON = "/html/body/div[4]/section/div/div/button[1]/span[1]"


class LogOutService:
    def __init__(self, driver):
        self.driver = driver

    def log_out(self):
        try:
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, SIGN_OUT_BUTTON))
            ).click()
        except ElementClickInterceptedException:
            self.log_out()

    def confirm_log_out(self):
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, CONFIRM_SIGN_OUT_BUTTON))
        ).click()
