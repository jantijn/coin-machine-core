import time

from factories.use_case_factory import build_web_driver
from factories.use_case_factory import build_login
from factories.use_case_factory import build_log_out
from factories.use_case_factory import build_get_next_filter
from factories.use_case_factory import build_refresh_transfer_list
from factories.use_case_factory import build_set_search_criteria
from factories.use_case_factory import build_bid_on_all_players_on_page
from factories.use_case_factory import build_list_all_transfer_targets

from services.logging_service import LoggingService

from entities.user_entity import user


class MassBidBot:
    def __init__(self, logging_service):
        self.logging_service = logging_service

    def run(self, username, password):
        web_driver = build_web_driver()
        log_in = build_login(web_driver)
        log_out = build_log_out(web_driver)
        get_next_filter = build_get_next_filter()
        refresh_transfer_list = build_refresh_transfer_list(web_driver)
        set_search_criteria = build_set_search_criteria(web_driver)
        bid_on_all_players_on_page = build_bid_on_all_players_on_page(web_driver)
        list_all_transfer_targets = build_list_all_transfer_targets(web_driver)

        user.set_username(username)
        user.set_app_password(password)

        log_in(user)
        filters = get_next_filter()

        timeout = time.time() + 1 * 60 * 60

        while time.time() < timeout:
            refresh_transfer_list()
            for filter in filters:
                set_search_criteria(filter, bid=True)
                bid_on_all_players_on_page(filter.max_buy_now_price, max_items = 10, max_time_left = 5  )
            time.sleep(5 * 60)
            list_all_transfer_targets(filters)

mass_bid_bot = MassBidBot(logging_service=LoggingService)
