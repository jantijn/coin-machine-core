from interfaces.logger.console import LoggerInterface
from interfaces.market_data.futbin import MarketDataInterface
from interfaces.purchased_items.ignore import PurchasedItemInterface
from interfaces.random_items.in_memory import RandomItemsInterface
from interfaces.web_app.selenium import WebAppInterface
from interfaces.web_app.selenium._app import initialize
from use_cases.login import Login
from use_cases.mass_bid import MassBid
from use_cases.verify_device import VerifyDevice

driver = initialize(headless=False)
web_app = WebAppInterface(driver, verbose=True)
random_items = RandomItemsInterface()
market_data = MarketDataInterface()
purchased_items = PurchasedItemInterface()
logger = LoggerInterface()

if __name__ == "__main__":
    login = Login(web_app, logger)
    print(login.execute("traderrr.joe@gmail.com", "H0p3l1jk"))

    verification_code = input("Enter verification code: ")

    verify_device = VerifyDevice(web_app, logger)
    print(verify_device.execute(verification_code))

    mass_bid = MassBid(web_app, random_items, market_data, purchased_items, logger)
    mass_bid.execute()
