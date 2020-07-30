import unittest

import entities.search_filter as search_filter

TEST_PLAYER = {
    "name": "Moussa Sissoko",
    "futbin_id": 183394,
    "margin": 100,
    "bonus": 100,
}
TEST_MARKET_PRICE = 2000


class TestSearchFilter(unittest.TestCase):
    def test_filter_init(self):
        et = search_filter.SearchFilter(
            name=TEST_PLAYER["name"], margin=TEST_PLAYER["margin"], bonus=TEST_PLAYER["bonus"],
        )

        assert et.name == TEST_PLAYER["name"]
        assert et.margin == TEST_PLAYER["margin"]
        assert et.bonus == TEST_PLAYER["bonus"]

    def test_filter_from_dict(self):
        et = search_filter.SearchFilter.from_dict(TEST_PLAYER)

        assert et.name == TEST_PLAYER["name"]
        assert et.margin == TEST_PLAYER["margin"]
        assert et.bonus == TEST_PLAYER["bonus"]

    def test_filter_calculate_prices(self):
        et = search_filter.SearchFilter.from_dict(TEST_PLAYER)

        et.calculate_prices(TEST_MARKET_PRICE)

        assert et.sell_price == TEST_MARKET_PRICE + TEST_PLAYER["bonus"]
        assert et.buy_price == int(TEST_MARKET_PRICE * 0.95 - TEST_PLAYER["margin"])
        assert isinstance(et.sell_price, int)
        assert isinstance(et.buy_price, int)

    def test_filter_to_dict(self):
        expected_result = dict(
            name=TEST_PLAYER["name"],
            max_buy_now_price=TEST_MARKET_PRICE * 0.95 - TEST_PLAYER["margin"],
            sell_price=TEST_MARKET_PRICE + TEST_PLAYER["bonus"],
        )

        et = search_filter.SearchFilter.from_dict(TEST_PLAYER)
        et.calculate_prices(TEST_MARKET_PRICE)

        assert et.to_dict() == expected_result
