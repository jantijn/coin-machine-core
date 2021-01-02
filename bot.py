from use_cases.list_transfer_list_items import ListTransferListItems
from use_cases.mass_bid import MassBid
from use_cases.login import Login
from use_cases.verify_device import VerifyDevice


class Bot:
    def __init__(self, web_app, logger, market_data, repository):
        self.web_app = web_app
        self.logger = logger
        self.market_data = market_data
        self.repository = repository
        self.username = None
        self.password = None

    def login(self):
        login = Login(web_app=self.web_app, logger=self.logger)
        return login.execute(self.username, self.password)

    def verify_device(self, verification_code):
        verify_device = VerifyDevice(web_app=self.web_app, logger=self.logger)
        return verify_device.execute(verification_code=verification_code)

    def mass_bid(self, **kwargs):
        options = {
            "margin": 300,
            "bonus": 0,
            "repetitions": 1,
            "max_total": 30,
            "max_time_left": 5,
            "max_per_cycle": 15,
        }
        options.update(kwargs)

        mass_bid = MassBid(
            web_app=self.web_app, repository=self.repository, logger=self.logger
        )
        return mass_bid.execute(
            margin=options["margin"],
            bonus=options["bonus"],
            repetitions=options["repetitions"],
            max_total=options["max_total"],
            max_time_left=options["max_time_left"],
            max_per_cycle=options["max_per_cycle"],
        )

    def list_transfer_list_items(self):
        list_transfer_list_items = ListTransferListItems(
            web_app=self.web_app,
            logger=self.logger,
            repository=self.repository,
            market_data=self.market_data,
        )
        list_transfer_list_items.execute(type_of_item="available_items")
        self.logger.log("Bot finished successfully!")

    def list_expired_transfer_list_items(self):
        list_transfer_list_items = ListTransferListItems(
            web_app=self.web_app,
            logger=self.logger,
            repository=self.repository,
            market_data=self.market_data,
        )
        list_transfer_list_items.execute(type_of_item="expired_items")
        self.logger.log("Bot finished successfully!")
