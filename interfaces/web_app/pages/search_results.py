import random
import time

from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, \
    StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from interfaces.web_app.pages import utils
from interfaces.web_app.pages.utils import WebAppElement

SEARCH_RESULTS = "li.listFUTItem.has-auction-data"
BID_PRICE_FIELD = "div.DetailPanel > div.bidOptions > div > input"
BID_BUTTON = "button.btn-standard.call-to-action.bidButton"
TIME_LEFT_LABEL = "span.time"
NAME = "div.name"
RATING = "div.rating"
BUY_NOW_BUTTON = "body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div > div > div.DetailPanel > div.bidOptions > button.btn-standard.buyButton.currency-coins"
CONFIRM_BUY_NOW_BUTTON = "body > div.view-modal-container.form-modal > section > div > div > button:nth-child(1)"
SEND_TO_CLUB_BUTTON = "body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div > div > div.DetailPanel > div.ut-button-group > button:nth-child(6)"
SEND_TO_TRANSFER_LIST_BUTTON = "body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div > div > div.DetailPanel > div.ut-button-group > button:nth-child(8)"
NAME_FIELD = "div.name.main-view"
PURCHASE_PRICE_FIELD = "div.auctionInfo > div > span.currency-coins.subContent"
LIST_ON_TRANSFER_MARKET_BUTTON = "body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div > div > div.DetailPanel > div.ut-quick-list-panel-view > div.ut-button-group > button"
OPEN_LIST_DIALOG_BUTTON = "div.DetailPanel > div.ut-quick-list-panel-view > div.ut-button-group > button > span.btn-text"
START_PRICE_FIELD = "div.DetailPanel > div.ut-quick-list-panel-view > div.panelActions.open > div:nth-child(2) > div.ut-numeric-input-spinner-control > input"
MAX_BUY_NOW_FIELD = "div.DetailPanel > div.ut-quick-list-panel-view > div.panelActions.open > div:nth-child(3) > div.ut-numeric-input-spinner-control > input"
CONFIRM_LISTING_BUTTON = "div.DetailPanel > div.ut-quick-list-panel-view > div.panelActions.open > button"

SNIPED_ITEM = "div.DetailView"
SNIPED_ITEM_NAME = "div.name"
SNIPED_ITEM_POSITION = "div.position"
SNIPED_ITEM_RATING = "div.rating"
SNIPED_ITEM_PURCHASE_PRICE = "span.currency-coins.subContent"


class SearchResult(WebAppElement):
    def __init__(self, driver, selenium_element):
        super().__init__(driver, selenium_element)
        self.name = self.get_attribute(NAME)
        self.rating = self.get_attribute(RATING)
        self.bid_price = None
        self.time_left = self._get_time_left()

    def bid(self, price):
        try:
            self.bid_price = price

            self.slow_click()
            self.slow_click()

            bid_price_field = utils.get_element(self.driver, BID_PRICE_FIELD)
            bid_price_string = bid_price_field.selenium_element.get_attribute("value")
            bid_price = int(bid_price_string.replace(',', ''))
            if bid_price > price:
                return False
            bid_price_field.safe_fill(price)

            bid_button = utils.get_element(self.driver, BID_BUTTON)
            bid_button.slow_click()
        except:
            pass

    def to_dict(self):
        return dict(name=self.name, rating=self.rating, bid_price=self.bid_price)

    def _get_time_left(self):
        time_left_string = self.get_attribute(TIME_LEFT_LABEL)
        return self._to_number(time_left_string)

    @staticmethod
    def _to_number(time_left_string):
        try:
            number = time_left_string.split(" ")[0].replace("<", "")
            unit = time_left_string.split(" ")[1]
        except:
            return 60
        if unit == "Seconds":
            return 1
        elif unit == "Hours" or unit == "Hour":
            return 60
        return int(number)


def bid_on_search_results(driver, price, max_bids, max_time_left):
    _random_pause(2)
    items_with_bid = []

    search_results = utils.get_elements(driver, SEARCH_RESULTS, class_=SearchResult)

    for search_result in search_results:
        _random_pause(1)
        if len(items_with_bid) >= max_bids or search_result.time_left >= max_time_left:
            break
        if "highest-bid" in search_result.get_classes():
            continue

        search_result.bid(price)
        items_with_bid.append(search_result.to_dict())

    return len(items_with_bid)


def _random_pause(average_pause_time_in_seconds):
    time.sleep(average_pause_time_in_seconds + random.uniform(-0.5, 0.5))


def outbid_by_other_player(driver):
    try:
        WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "Notification"))
        ).click()
        WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "icon_close"))
        ).click()
    except TimeoutException:
        return False
    except:
        return True
    return True


def buy_now(driver):
    try:
        WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "buyButton"))
        ).click()
    except TimeoutException:
        return False
    except ElementClickInterceptedException:
        buy_now(driver)
    except StaleElementReferenceException:
        buy_now(driver)
    return True


def confirm_buy_now(driver):
    try:
        WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/ html / body / div[4] / section / div / div / button[1]",
                )
            )
        ).click()
    except TimeoutException:
        return False
    return True


def get_sniped_item(driver):
    sniped_item = utils.get_element(
        driver, SNIPED_ITEM
    )
    return sniped_item


def send_to_club(driver):
    send_to_club_button = utils.get_element(
        driver, SEND_TO_CLUB_BUTTON
    )
    send_to_club_button.slow_click()


def send_to_transfer_list(driver):
    send_to_transfer_list_button = utils.get_element(
        driver, SEND_TO_TRANSFER_LIST_BUTTON
    )
    send_to_transfer_list_button.slow_click()


def list(driver, price):
    open_list_dialog(driver)
    set_start_price(driver, price - 100)
    set_max_buy_now_price(driver, price)
    confirm_listing(driver)


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


def get_name(driver):
    name_field = utils.get_element(
        driver, NAME_FIELD
    )
    return name_field.get_text()


def get_purchase_price(driver):
    purchase_price_field = utils.get_element(
        driver, PURCHASE_PRICE_FIELD
    )
    return purchase_price_field.get_text()

def get_search_results(driver):
    return utils.get_elements(driver, SEARCH_RESULTS)
