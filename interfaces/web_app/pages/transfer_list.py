from interfaces.web_app.pages import utils

REMOVE_SOLD_ITEMS_BUTTON = "div.ut-navigation-container-view--content > div > div > div > section:nth-child(1) > header > button"
RELIST_UNSOLD_ITEMS_BUTTON = "div.ut-navigation-container-view--content > div > div > div > section:nth-child(2) > header > button"
CONFIRM_RELIST_BUTTON = "body > div.view-modal-container.form-modal > section > div > div > button:nth-child(2)"
AVAILABLE_ITEMS = "section:nth-child(3) > ul > li"
EXPIRED_ITEMS = "li.listFUTItem.has-auction-data.expired"
OPEN_LIST_DIALOG_BUTTON = (
    "div.DetailPanel > div.ut-quick-list-panel-view > div.ut-button-group > button"
)
START_PRICE_FIELD = "div.panelActions.open > div:nth-child(2) > div.ut-numeric-input-spinner-control > input"
MAX_BUY_NOW_FIELD = "div.DetailPanel > div.ut-quick-list-panel-view > div.panelActions.open > div:nth-child(3) > div.ut-numeric-input-spinner-control > input"
CONFIRM_LISTING_BUTTON = (
    "div.DetailPanel > div.ut-quick-list-panel-view > div.panelActions.open > button"
)
NAME = "div.name"
RATING = "div.rating"
POSITION = "div.position"


def remove_sold_items(driver):
    if utils.element_exists(driver, REMOVE_SOLD_ITEMS_BUTTON):
        go_to_transfers_button = utils.get_element(driver, REMOVE_SOLD_ITEMS_BUTTON)
        go_to_transfers_button.slow_click()


def relist_unsold_items(driver):
    if utils.element_exists(driver, RELIST_UNSOLD_ITEMS_BUTTON):
        relist_unsold_items_button = utils.get_element(
            driver, RELIST_UNSOLD_ITEMS_BUTTON
        )
        relist_unsold_items_button.slow_click()

        confirm_relist_button = utils.get_element(driver, CONFIRM_RELIST_BUTTON)
        confirm_relist_button.slow_click()


def get_available_items(driver, type_of_item):
    if type_of_item == "available_items":
        return utils.get_elements(driver, AVAILABLE_ITEMS)
    elif type_of_item == "expired_items":
        return utils.get_elements(driver, EXPIRED_ITEMS)


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
