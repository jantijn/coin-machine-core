from interfaces.web_app.pages import utils

GO_TO_TRANSFER_LIST_BUTTON = "div.ut-tile-transfer-list"
GO_TO_SEARCH_THE_TRANSFER_MARKET_BUTTON = "div.ut-tile-transfer-market"
GO_TO_TRANSFER_TARGETS_BUTTON = "div.tile.col-1-2.ut-tile-transfer-targets"


def go_to_transfer_list(driver):
    go_to_transfer_list_button = utils.get_element(driver, GO_TO_TRANSFER_LIST_BUTTON)
    go_to_transfer_list_button.safe_click()


def go_to_search_the_transfer_market(driver):
    go_to_search_the_transfer_market_button = utils.get_element(
        driver, GO_TO_SEARCH_THE_TRANSFER_MARKET_BUTTON
    )
    go_to_search_the_transfer_market_button.safe_click()


def go_to_transfer_targets(driver):
    go_to_transfer_targets_button = utils.get_element(
        driver, GO_TO_TRANSFER_TARGETS_BUTTON
    )
    go_to_transfer_targets_button.safe_click()
