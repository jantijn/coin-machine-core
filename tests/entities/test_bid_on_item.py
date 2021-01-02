import unittest

import entities.bid_on_item as bid_on_item

TEST_PLAYER = {
    "name": "Moussa Sissoko",
    "bid": 2000,
}


class TestBidOnItem(unittest.TestCase):
    def test_bid_on_item_init(self):
        et = bid_on_item.BidOnItem(
            name=TEST_PLAYER["name"],
            bid=TEST_PLAYER["bid"],
        )

        assert et.name == TEST_PLAYER["name"]
        assert et.bid == TEST_PLAYER["bid"]

    def test_filter_from_dict(self):
        et = bid_on_item.BidOnItem.from_dict(TEST_PLAYER)

        assert et.name == TEST_PLAYER["name"]
        assert et.bid == TEST_PLAYER["bid"]

    def test_filter_to_dict(self):
        expected_result = dict(
            name=TEST_PLAYER["name"],
            bid=TEST_PLAYER["bid"],
        )

        et = bid_on_item.BidOnItem.from_dict(TEST_PLAYER)

        assert et.to_dict() == expected_result
