from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def build_web_driver(headless):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(
        ChromeDriverManager().install(),
        chrome_options=chrome_options
    )
    driver.get("https://easports.com/fifa/ultimate-team/web-app/")

    return driver
