import unittest

import entities.purchased_item as purchased_item

TEST_PLAYER = {
    "name": "Moussa Sissoko",
    "purchase_price": 1000,
    "sell_price": 2000,
}


def calculate_profit(purchase_price, sell_price):
    return int(round((sell_price * 0.95 - purchase_price) / 100, 0) * 100)


class TestPurchasedItem(unittest.TestCase):
    def test_purchased_item_init(self):
        et = purchased_item.PurchasedItem(
            name=TEST_PLAYER["name"],
            purchase_price=TEST_PLAYER["purchase_price"],
            sell_price=TEST_PLAYER["sell_price"],
        )

        assert et.name == TEST_PLAYER["name"]
        assert et.purchase_price == TEST_PLAYER["purchase_price"]
        assert et.sell_price == TEST_PLAYER["sell_price"]
        assert et.profit == calculate_profit(TEST_PLAYER["purchase_price"], TEST_PLAYER["sell_price"])

    def test_purchased_item_from_dict(self):
        et = purchased_item.PurchasedItem.from_dict(TEST_PLAYER)

        assert et.name == TEST_PLAYER["name"]
        assert et.purchase_price == TEST_PLAYER["purchase_price"]
        assert et.sell_price == TEST_PLAYER["sell_price"]
        assert et.profit == calculate_profit(TEST_PLAYER["purchase_price"], TEST_PLAYER["sell_price"])

    def test_purchased_item_to_dict(self):
        expected_result = dict(
            name=TEST_PLAYER["name"],
            purchase_price=TEST_PLAYER["purchase_price"],
            sell_price=TEST_PLAYER["sell_price"],
            profit=calculate_profit(TEST_PLAYER["purchase_price"], TEST_PLAYER["sell_price"]),
        )

        et = purchased_item.PurchasedItem.from_dict(TEST_PLAYER)

        assert et.to_dict() == expected_result
