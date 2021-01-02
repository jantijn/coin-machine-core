from interfaces.web_app.pages import utils


SEARCH_RESULTS = "li.listFUTItem.has-auction-data"
BID_PRICE_FIELD = "div.DetailPanel > div.bidOptions > div > input"
BID_BUTTON = "button.btn-standard.call-to-action.bidButton"
TIME_LEFT_LABEL = "span.time"
NAME = "div.name"
RATING = "div.rating"


def get_search_results(driver):
    return utils.get_elements(driver, SEARCH_RESULTS)


def set_bid_price(driver, price):
    bid_price_field = utils.get_element(driver, BID_PRICE_FIELD)
    bid_price_field.safe_fill(price)


def place_bid(driver):
    bid_button = utils.get_element(driver, BID_BUTTON)
    bid_button.slow_click()
