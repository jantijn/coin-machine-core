from interfaces.web_app.pages import utils

NAME_FIELD = "body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-pinned-list-container.ut-content-container > div > div.ut-pinned-list > div.ut-item-search-view > div.inline-list-select.ut-player-search-control > div > div.ut-player-search-control--input-container > input"
NAME_BUTTON = "body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-pinned-list-container.ut-content-container > div > div.ut-pinned-list > div.ut-item-search-view > div.inline-list-select.ut-player-search-control.has-selection.contract-text-input.is-open > div > div.inline-list > ul > button:nth-child(1)"
MAX_BID_PRICE_FIELD = "body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-pinned-list-container.ut-content-container > div > div.ut-pinned-list > div.search-prices > div:nth-child(3) > div.ut-numeric-input-spinner-control > input"
MIN_BID_PRICE_FIELD = "body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-pinned-list-container.ut-content-container > div > div.ut-pinned-list > div.search-prices > div:nth-child(2) > div.ut-numeric-input-spinner-control > input"
MAX_BUY_NOW_PRICE_FIELD = "body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-pinned-list-container.ut-content-container > div > div.ut-pinned-list > div.search-prices > div:nth-child(6) > div.ut-numeric-input-spinner-control > input"
SEARCH_THE_TRANSFER_MARKET_BUTTON = "button.btn-standard.call-to-action"
GO_BACK_BUTTON = "body > main > section > section > div.ut-navigation-bar-view.navbar-style-landscape > button.ut-navigation-button-control"
CLUB_BUTTON = "body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-pinned-list-container.ut-content-container > div > div.ut-pinned-list > div.ut-item-search-view > div:nth-child(8)"
CHARACTERISTICS = "li.with-icon"
NATION_BUTTON = "body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-pinned-list-container.ut-content-container > div > div.ut-pinned-list > div.ut-item-search-view > div:nth-child(6)"
POSITION_BUTTON = "body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-pinned-list-container.ut-content-container > div > div.ut-pinned-list > div.ut-item-search-view > div:nth-child(4)"
INCREMENT_MIN_BID_PRICE_BUTTON = "body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-pinned-list-container.ut-content-container > div > div.ut-pinned-list > div.search-prices > div:nth-child(2) > div.ut-numeric-input-spinner-control > button.btn-standard.increment-value"
DECREMENT_MIN_BID_PRICE_BUTTON = "body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-pinned-list-container.ut-content-container > div > div.ut-pinned-list > div.search-prices > div:nth-child(2) > div.ut-numeric-input-spinner-control > button.btn-standard.decrement-value"

def set_bid_filter(driver, name, price):
    name_field = utils.get_element(driver, NAME_FIELD)
    name_field.safe_fill(name)

    name_button = utils.get_element(driver, NAME_BUTTON)
    name_button.slow_click()

    max_bid_price_field = utils.get_element(driver, MAX_BID_PRICE_FIELD)
    max_bid_price_field.safe_fill(price - 100)


def set_snipe_filter(driver, name, price):
    name_field = utils.get_element(driver, NAME_FIELD)
    name_field.safe_fill(name)

    name_button = utils.get_element(driver, NAME_BUTTON)
    name_button.slow_click()

    _set_price_fields(driver, price)


def set_snipe_filter_based_on_characteristics(driver, club, nation, position, price):
    _set_club_field(club, driver)
    _set_nation_field(nation, driver)
    _set_position_field(position, driver)
    _set_price_fields(driver, price)


def _set_club_field(club, driver):
    club_button = utils.get_element(driver, CLUB_BUTTON)
    club_button.slow_click()
    clubs = utils.get_elements(driver, CHARACTERISTICS)

    for club_element in clubs:
        if club in club_element.get_text():
            club_element.slow_click()
            break


def _set_nation_field(nation, driver):
    nation_button = utils.get_element(driver, NATION_BUTTON)
    nation_button.slow_click()
    nations = utils.get_elements(driver, CHARACTERISTICS)

    for nation_element in nations:
        if nation in nation_element.get_text():
            nation_element.slow_click()
            break


def _set_position_field(position, driver):
    position_button = utils.get_element(driver, POSITION_BUTTON)
    position_button.slow_click()
    positions = utils.get_elements(driver, CHARACTERISTICS)

    for position_element in positions:
        if position in position_element.get_text():
            position_element.slow_click()
            break
            

def _set_price_fields(driver, price):
    max_buy_now_price_field = utils.get_element(driver, MAX_BUY_NOW_PRICE_FIELD)
    max_buy_now_price_field.safe_fill(price)
    set_min_bid_price(driver, price = 150)


def set_min_bid_price(driver, price):
    min_bid_price_field = utils.get_element(driver, MIN_BID_PRICE_FIELD)
    min_bid_price_field.fast_fill(price)


def increment_min_bid_price(driver):
    increment_min_bid_price_button = utils.get_element(
        driver, INCREMENT_MIN_BID_PRICE_BUTTON
    )
    increment_min_bid_price_button.fast_click()


def decrement_min_bid_price(driver):
    decrement_min_bid_price_button = utils.get_element(
        driver, DECREMENT_MIN_BID_PRICE_BUTTON
    )
    decrement_min_bid_price_button.fast_click()


def search_the_transfer_market(driver):
    search_the_transfer_market_button = utils.get_element(
        driver, SEARCH_THE_TRANSFER_MARKET_BUTTON
    )
    search_the_transfer_market_button.slow_click()


def go_back(driver):
    go_back_button = utils.get_element(
        driver, GO_BACK_BUTTON
    )
    go_back_button.slow_click()
