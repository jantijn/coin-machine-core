from interfaces.web_app.pages import utils

NAME_FIELD = "body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-pinned-list-container.ut-content-container > div > div.ut-pinned-list > div.ut-item-search-view > div.inline-list-select.ut-player-search-control > div > div.ut-player-search-control--input-container > input"
NAME_BUTTON = "body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-pinned-list-container.ut-content-container > div > div.ut-pinned-list > div.ut-item-search-view > div.inline-list-select.ut-player-search-control.has-selection.contract-text-input.is-open > div > div.inline-list > ul > button:nth-child(1)"
MAX_BID_PRICE_FIELD = "body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-pinned-list-container.ut-content-container > div > div.ut-pinned-list > div.search-prices > div:nth-child(3) > div.ut-numeric-input-spinner-control > input"
SEARCH_THE_TRANSFER_MARKET_BUTTON = "button.btn-standard.call-to-action"


def set_bid_filter(driver, name, price):
    name_field = utils.get_element(driver, NAME_FIELD)
    name_field.safe_fill(name)

    name_button = utils.get_element(driver, NAME_BUTTON)
    name_button.slow_click()

    max_bid_price_field = utils.get_element(driver, MAX_BID_PRICE_FIELD)
    max_bid_price_field.safe_fill(price - 100)


def search_the_transfer_market(driver):
    search_the_transfer_market_button = utils.get_element(
        driver, SEARCH_THE_TRANSFER_MARKET_BUTTON
    )
    search_the_transfer_market_button.slow_click()
