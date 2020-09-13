import pickle
from cmd import Cmd

import selenium.webdriver

from interfaces.logger.console import LoggerInterface
from interfaces.market_data.futbin import MarketDataInterface
from interfaces.purchased_items.ignore import PurchasedItemInterface
from interfaces.random_items.in_memory import RandomItemsInterface
from interfaces.web_app.selenium import WebAppInterface
from use_cases.refresh_transfer_list import RefreshTransferList
from use_cases.login import Login
from use_cases.verify_device import VerifyDevice

web_app = WebAppInterface()
random_items = RandomItemsInterface()
market_data = MarketDataInterface()
purchased_items = PurchasedItemInterface()
logger = LoggerInterface()

EXECUTOR = 'http://192.168.2.120:4444/wd/hub'
FILENAME = '/tmp/pickle'


class MyPrompt(Cmd):
    prompt = 'pb> '
    intro = "Welcome! Type ? to list commands"

    def do_new_driver(self, arg):
        opt = selenium.webdriver.chrome.options.Options()
        capabilities = opt.to_capabilities()
        self.driver = selenium.webdriver.Remote(command_executor = EXECUTOR, desired_capabilities = capabilities)
        self.driver.get("https://easports.com/fifa/ultimate-team/web-app/")
        #
        # self.driver = _initialize(headless = False) if arg else _initialize(headless = True)
        self._set_driver(self.driver)

    def do_load_driver(self, arg):
        with open('driver.pickle', 'rb') as fp:
            self.driver = pickle.load(fp)
        self._set_driver(self.driver)

    def do_stop_driver(self, arg):
        self.driver.quit()

    def _set_driver(self, driver):
        web_app.set_driver(driver)
        print('Driver initialized!')

    def do_save_driver(self, arg):
        with open('driver.pickle', 'wb') as fp:
            pickle.dump(self.driver, fp)

    def do_login(self, arg):
        login = Login(web_app, logger)
        print(
            login.execute("traderrr.joe@gmail.com", "H0p3l1jk")
        )

    def do_verify_device(self, arg):
        verify_device = VerifyDevice(web_app, logger)
        print(
            verify_device.execute(verification_code = arg)
        )

    def do_refresh_transfer_list(self, arg):
        refresh_transfer_list = RefreshTransferList(web_app, logger)
        print(
            refresh_transfer_list.execute()
        )

    def do_exit(self, inp):
        print("Bye")
        return True

    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)

        print("Default: {}".format(inp))

    do_EOF = do_exit
    help_EOF = help_exit


if __name__ == '__main__':
    MyPrompt().cmdloop()