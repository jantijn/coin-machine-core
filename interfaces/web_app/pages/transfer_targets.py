from difflib import SequenceMatcher

from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementNotInteractableException,
)

from interfaces.web_app.pages import utils

CLEAR_BUTTON = "div.ut-navigation-container-view--content > div > div > div > section:nth-child(4) > header > button"
PURCHASED_ITEMS = "li.listFUTItem.has-auction-data.won"
NAME = "div.name"
RATING = "div.rating"
PURCHASE_PRICE = "div.auction > div:nth-child(2) > span.currency-coins.value"
OPEN_LIST_DIALOG_BUTTON = (
    "div.DetailPanel > div.ut-quick-list-panel-view > div.ut-button-group > button"
)
START_PRICE_FIELD = "div.DetailPanel > div.ut-quick-list-panel-view > div.panelActions.open > div:nth-child(2) > div.ut-numeric-input-spinner-control > input"
MAX_BUY_NOW_FIELD = "div.DetailPanel > div.ut-quick-list-panel-view > div.panelActions.open > div:nth-child(3) > div.ut-numeric-input-spinner-control > input"
CONFIRM_LISTING_BUTTON = (
    "div.DetailPanel > div.ut-quick-list-panel-view > div.panelActions.open > button"
)


def open_list_dialog(driver):
    open_list_dialog_button = utils.get_element(driver, OPEN_LIST_DIALOG_BUTTON)
    open_list_dialog_button.slow_click()


def set_start_price(driver, price):
    start_price_field = utils.get_element(driver, START_PRICE_FIELD)
    start_price_field.safe_fill(price)


def set_max_buy_now_price(driver, price):
    max_buy_now_field = utils.get_element(driver, MAX_BUY_NOW_FIELD)
    max_buy_now_field.safe_fill(price)


def confirm_listing(driver):
    open_list_dialog_button = utils.get_element(driver, CONFIRM_LISTING_BUTTON)
    open_list_dialog_button.slow_click()


def clear_expired_players(driver):
    if utils.element_exists(driver, CLEAR_BUTTON):
        clear_expired_players_button = utils.get_element(driver, CLEAR_BUTTON)
        clear_expired_players_button.slow_click()


def get_won_items(driver):
    return utils.get_elements(driver, PURCHASED_ITEMS)
