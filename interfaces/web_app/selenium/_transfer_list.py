from interfaces.web_app.selenium import utils

REMOVE_SOLD_ITEMS_BUTTON = (
    "div.ut-navigation-container-view--content > div > div > div > section:nth-child(1) > header > button"
)
RELIST_UNSOLD_ITEMS_BUTTON = (
    "div.ut-navigation-container-view--content > div > div > div > section:nth-child(2) > header > button"
)
CONFIRM_RELIST_BUTTON = "body > div.view-modal-container.form-modal > section > div > div > button:nth-child(2)"


def remove_sold_items(driver):
    if utils.element_exists(driver, REMOVE_SOLD_ITEMS_BUTTON):
        go_to_transfers_button = utils.get_element(driver, REMOVE_SOLD_ITEMS_BUTTON)
        go_to_transfers_button.slow_click()


def relist_unsold_items(driver):
    if utils.element_exists(driver, RELIST_UNSOLD_ITEMS_BUTTON):
        relist_unsold_items_button = utils.get_element(driver, RELIST_UNSOLD_ITEMS_BUTTON)
        relist_unsold_items_button.slow_click()

        confirm_relist_button = utils.get_element(driver, CONFIRM_RELIST_BUTTON)
        confirm_relist_button.slow_click()
