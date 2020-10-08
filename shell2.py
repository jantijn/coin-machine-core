import pickle
from cmd import Cmd

import selenium.webdriver

from interfaces.logger import Logger
from interfaces.market_data import MarketData
from interfaces.repository.django import Repository
from interfaces.web_app import WebApp
from use_cases.bid_on_each_search_filter import BidOnEachSearchFilter
from use_cases.get_search_filters import GetSearchFilters
from use_cases.list_transfer_list_items import ListTransferListItems
from use_cases.list_won_items import ListWonItems
from use_cases.logout import Logout
from use_cases.refresh_transfer_list import RefreshTransferList
from use_cases.login import Login
from use_cases.verify_device import VerifyDevice

from bot import Bot

# docker run -d -p 4444:4444 -p 5900:5900 -v /dev/shm:/dev/shm selenium/standalone-chrome:4.0.0-alpha-7-prerelease-20200907
# open vnc://0.0.0.0:5900

web_app = WebApp(custom_driver=True)
market_data = MarketData()
repository = Repository()
repository.login(username = "admin", password = "J@nt1jn+admin")
logger = Logger()

EXECUTOR = "http://localhost:4444/wd/hub"
FILENAME = "/tmp/pickle"

state = {"search_filters": ""}


class MyPrompt(Cmd):
    prompt = "-> "
    intro = "Welcome! Type ? to list commands"

    def do_new_driver(self, arg):
        opt = selenium.webdriver.chrome.options.Options()
        capabilities = opt.to_capabilities()
        self.driver = selenium.webdriver.Remote(
            command_executor=EXECUTOR, desired_capabilities=capabilities
        )
        self.driver.get("https://easports.com/fifa/ultimate-team/web-app/")
        self._set_driver(self.driver)

    def do_load_driver(self, arg):
        with open("driver.pickle", "rb") as fp:
            self.driver = pickle.load(fp)
        self._set_driver(self.driver)

    def do_stop_driver(self, arg):
        self.driver.quit()

    def _set_driver(self, driver):
        web_app.set_driver(driver)
        print("Driver initialized!")

    def do_save_driver(self, arg):
        with open("driver.pickle", "wb") as fp:
            pickle.dump(self.driver, fp)

    def do_login(self, arg):
        login = Login(web_app, logger)
        print(login.execute("jantijn.kromwijk@gmail.com", "H0p3l1jk"))

    def do_verify_device(self, arg):
        verify_device = VerifyDevice(web_app, logger)
        print(verify_device.execute(verification_code=arg))

    def do_refresh_transfer_list(self, arg):
        refresh_transfer_list = RefreshTransferList(web_app, logger)
        refresh_transfer_list.execute()

    def do_get_search_filters(self, arg):
        get_search_filters = GetSearchFilters(
            repository=repository, market_data=market_data, logger=logger
        )
        state["search_filters"] = get_search_filters.execute(number_of_search_filters=4, margin=100)

    def do_bid_on_each_search_filter(self, arg):
        if state["search_filters"]:
            bid_on_each_search_filter = BidOnEachSearchFilter(
                web_app=web_app, logger=logger
            )
            bid_on_each_search_filter.execute(
                search_filters=state["search_filters"], max_time_left=25
            )
        else:
            print("First load search filters")

    def do_list_won_items(self, arg):
        list_won_items = ListWonItems(
            web_app=web_app, logger=logger, repository=repository
        )
        list_won_items.execute(margin=200, bonus=100)

    def do_list_transfer_list_items(self, arg):
        list_transfer_list_items = ListTransferListItems(
            web_app = web_app, logger = logger, repository = repository, market_data = market_data
        )
        list_transfer_list_items.execute()

    def do_logout(self, arg):
        logout = Logout(web_app=web_app, logger=logger)
        logout.execute()

    def do_exit(self, inp):
        print("Bye")
        return True

    def help_exit(self):
        print("exit the application. Shorthand: x q Ctrl-D.")

    def default(self, inp):
        if inp == "x" or inp == "q":
            return self.do_exit(inp)

        print("Default: {}".format(inp))

    do_EOF = do_exit
    help_EOF = help_exit


if __name__ == "__main__":
    MyPrompt().cmdloop()
