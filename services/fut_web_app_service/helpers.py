from selenium.webdriver.common.keys import Keys


def safe_fill(element, text, manual_reset=False):
    while element.get_attribute("value") != text:

        if manual_reset:
            element.send_keys(Keys.BACK_SPACE)
            element.send_keys(Keys.DELETE)

        element.clear()
        element.send_keys(text)
