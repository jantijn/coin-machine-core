from .executors import (
    LoginExecutor,
    VerifyDeviceExecutor,
    RefreshTransferListExecutor,
    BidOnSearchFilterItemsExecutor,
    ListAllTransferTargetsExecutor,
)
from .web_app_objects import WonItem


class WebAppInterface:
    def __init__(self, driver):
        self.driver = driver

    def login(self, email, password):
        LoginExecutor(self.driver).login(email, password)

    def verify_device(self, verification_code):
        VerifyDeviceExecutor(self.driver).verify_device(verification_code)

    def refresh_transfer_list(self):
        RefreshTransferListExecutor(self.driver).refresh_transfer_list()

    def bid_on_search_filter_items(self, price):
        BidOnSearchFilterItemsExecutor(self.driver).bid_on_search_filter_items(price)

    def list_all_transfer_targets(self, search_filters):
        won_items = ListAllTransferTargetsExecutor(
            self.driver
        ).list_all_transfer_targets(search_filters)
        return self._to_won_item_entity(won_items)

    @staticmethod
    def _to_won_item_entity(won_items):
        data = []
        for won_item in won_items:
            data.append(WonItem.from_dict(won_item))
        return data
