from use_cases.bid_on_items import BidOnItems
from use_cases.enter_verification_code import EnterVerificationCode
from use_cases.get_filters import GetFilters
from use_cases.handle_error import HandleError
from use_cases.list_all_transfer_targets import ListAllTransferTargets
from use_cases.login import Login
from use_cases.logout import Logout
from use_cases.refresh_transfer_list import RefreshTransferList
from use_cases.set_search_criteria import SetSearchCriteria
from use_cases.snipe_player import SnipePlayer


def build_bid_on_all_players_on_page(fut_web_app_service, logging_service):
    return BidOnItems(
        fut_web_app_service = fut_web_app_service,
        logging_service = logging_service,
    ).execute


def build_enter_verification_code(fut_web_app_service, logging_service):
    return EnterVerificationCode(
        fut_web_app_service = fut_web_app_service,
        logging_service = logging_service,
    ).execute


def build_get_filters(database_service, market_price_service, logging_service):
    return GetFilters(
        database_service = database_service,
        market_price_service = market_price_service,
        logging_service = logging_service,
    ).execute


def build_handle_error(fut_web_app_service, logging_service):
    return HandleError(
        fut_web_app_service = fut_web_app_service,
        logging_service = logging_service,
    ).execute


def build_list_all_transfer_targets(fut_web_app_service, database_service, logging_service):
    return ListAllTransferTargets(
        fut_web_app_service = fut_web_app_service,
        database_service = database_service,
        logging_service = logging_service,
    ).execute


def build_login(fut_web_app_service, logging_service):
    return Login(
        fut_web_app_service = fut_web_app_service,
        logging_service = logging_service,
    ).execute


def build_logout(fut_web_app_service, logging_service):
    return Logout(
        fut_web_app_service = fut_web_app_service,
        logging_service = logging_service
    ).execute


def build_refresh_transfer_list(fut_web_app_service, logging_service):
    return RefreshTransferList(
        fut_web_app_service = fut_web_app_service,
        logging_service = logging_service
    ).execute


def build_set_search_criteria(fut_web_app_service, logging_service):
    return SetSearchCriteria(
        fut_web_app_service = fut_web_app_service,
        logging_service = logging_service,
    ).execute


def build_snipe_player(fut_web_app_service, database_service, logging_service):
    return SnipePlayer(
        fut_web_app_service = fut_web_app_service,
        database_service = database_service,
        logging_service = logging_service
    ).execute
