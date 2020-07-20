import time

from factories import use_case_factory as factories


class FutBot:
    def __init__(self, logging_service, database_service):
        self.driver = None
        self.logging_service = logging_service
        self.database_service = database_service

    def initialize(self, headless=True):
        self.driver = factories.build_web_driver(headless)

    def login(self, username, password):
        login = factories.build_login(self.driver)
        login(username = username, password = password)

    def enter_verification_code(self, verification_code):
        enter_verification_code = factories.build_enter_verification_code(self.driver)
        enter_verification_code(verification_code = verification_code)

    def mass_bid(self, duration):
        get_filters = factories.build_get_filters(self.database_service)
        refresh_transfer_list = factories.build_refresh_transfer_list(self.driver)
        set_search_criteria = factories.build_set_search_criteria(self.driver)
        bid_on_items = factories.build_bid_on_items(self.driver)
        list_all_transfer_targets = factories.build_list_all_transfer_targets(self.driver)

        timeout = time.time() + duration

        while time.time() < timeout:
            refresh_transfer_list()
            search_filters = get_filters(number = 3)
            for search_filter in search_filters:
                set_search_criteria(search_filter, bid = True)
                bid_on_items(search_filter.max_buy_now_price, max_items = 10, max_time_left = 5)
            time.sleep(5 * 60)
            list_all_transfer_targets(search_filters)
