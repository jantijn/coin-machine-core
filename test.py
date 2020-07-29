from bots.mass_bid_bot import MassBidBot
from interfaces.logger.console import LoggerInterface
from interfaces.market_data.futbin import MarketDataInterface
from interfaces.purchased_items.ignore import PurchasedItemInterface
from interfaces.random_items.in_memory import RandomItemsInterface
from interfaces.web_app.selenium import WebAppInterface
from interfaces.web_app.selenium.drivers import build_web_driver

driver = build_web_driver(headless=False)
web_app = WebAppInterface(driver)
random_items = RandomItemsInterface()
market_data = MarketDataInterface()
purchased_items = PurchasedItemInterface()
logger = LoggerInterface()

if __name__ == "__main__":
    bot = MassBidBot(
        web_app = web_app,
        random_items = random_items,
        market_data = market_data,
        purchased_items = purchased_items,
        logger = logger
    )

    bot.login('traderrr.joe@gmail.com', 'H0p3l1jk')
    verification_code = input('Enter verification code: ')
    bot.verify_device(verification_code)
    bot.mass_bid()
