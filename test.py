from factories.web_driver_factory import build_web_driver
from interfaces.web_app import WebAppInterface

if __name__ == "__main__":
    driver = build_web_driver(headless = False)
    fut_service = WebAppInterface(driver)
    fut_service.login('traderrr.joe@gmail.com', 'H0p3l1jk')