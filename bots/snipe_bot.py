import random
import time

from factories.use_case_factory import build_handle_error
from factories.use_case_factory import build_login
from factories.use_case_factory import build_log_out
from factories.use_case_factory import build_set_search_criteria
from factories.use_case_factory import build_snipe_player
from factories.use_case_factory import build_refresh_transfer_list
from factories.use_case_factory import build_get_next_filter
from factories.use_case_factory import build_web_driver

from services.logging_service import LoggingService

from entities.user_entity import user


class SnipeBot:
    def __init__(self, logging_service):
        self.logging_service = logging_service
        self.number_of_snipes = 0
        self.number_of_snipes_until_long_pause = (
            self._calculate_number_of_snipes_until_long_pause()
        )
        self.number_of_snipes_until_short_pause = (
            self._calculate_number_of_snipes_until_short_pause()
        )
        self.active_filter = {}
        self.keep_running = True


    def run(self, username, password, session_hash, token):
        self.timeout = time.time() + 3 * 60 * 60

        web_driver = build_web_driver()

        self._handle_error = build_handle_error(web_driver)
        self._log_in = build_login(web_driver, session_hash, token)
        self._log_out = build_log_out(web_driver)
        self._get_next_filter = build_get_next_filter(session_hash, token)
        self._set_search_criteria = build_set_search_criteria(web_driver)
        self._snipe_player = build_snipe_player(web_driver, session_hash, token)
        self._refresh_transfer_list = build_refresh_transfer_list(web_driver)

        user.set_username(username)
        user.set_app_password(password)

        self._log_in(user)
        self.active_filter = self._get_next_filter()
        self._start_sniper()

        while time.time() < self.timeout:
            if self.number_of_snipes_until_long_pause <= 0:
                self._long_pause()
            if self.number_of_snipes_until_short_pause <= 0:
                self._short_pause()

            self._log_current_state()

            try:
                self._snipe_player(self.active_filter)
            except:
                self._handle_error()
                self._start_sniper()

            self._update_state()

    def _start_sniper(self):
        self._refresh_transfer_list()
        self._set_search_criteria(self.active_filter)

    def _long_pause(self):
        pause = abs(int(random.gauss(3600, 600)))
        self._refresh_transfer_list()
        self._log_out()
        self._pause(pause)
        self._log_in(user)
        self._start_sniper()
        self.number_of_snipes_until_long_pause = (
            self._calculate_number_of_snipes_until_long_pause()
        )

    def _short_pause(self):
        pause = abs(int(random.gauss(30, 10)))
        self._pause(pause)
        self.number_of_snipes_until_short_pause = (
            self._calculate_number_of_snipes_until_short_pause()
        )

    def _pause(self, pause):
        self.logging_service.log("-" * 80)

        for seconds_remaining in range(pause, 0, -1):
            print(f"Pausing for {seconds_remaining} seconds")
            time.sleep(1)

        self.logging_service.log("")

    @staticmethod
    def _calculate_number_of_snipes_until_long_pause():
        return abs(int(random.gauss(450, 25)))

    @staticmethod
    def _calculate_number_of_snipes_until_short_pause():
        return abs(int(random.gauss(30, 10)))

    def _log_current_state(self):
        self.logging_service.log("")
        self.logging_service.log("-" * 80)
        self.logging_service.log("Snipe attempt number: " + str(self.number_of_snipes))
        self.logging_service.log(
            "Number of snipes until long pause: "
            + str(self.number_of_snipes_until_long_pause)
        )
        self.logging_service.log(
            "Number of snipes until short pause: "
            + str(self.number_of_snipes_until_short_pause)
        )
        self.logging_service.log("Time left: " + str(self.timeout - time.time()))

    def _update_state(self):
        self.number_of_snipes_until_long_pause = (
            self.number_of_snipes_until_long_pause - 1
        )
        self.number_of_snipes_until_short_pause = (
            self.number_of_snipes_until_short_pause - 1
        )
        self.number_of_snipes += 1


snipe_bot = SnipeBot(logging_service=LoggingService)
