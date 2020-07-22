import entities.search_filter_entity as search_filter_entity

TEST_PLAYER = {"name": "Moussa Sissoko", "futbin_id": 183394, "margin": 100, "bonus": 100}
TEST_MARKET_PRICE = 2000


def test_filter_entity_init():
    et = search_filter_entity.SearchFilterEntity(
        futbin_id=TEST_PLAYER["futbin_id"],
        name=TEST_PLAYER["name"],
        margin=TEST_PLAYER["margin"],
        bonus=TEST_PLAYER["bonus"],
    )

    assert et.name == TEST_PLAYER["name"]
    assert et.futbin_id == TEST_PLAYER["futbin_id"]
    assert et.margin == TEST_PLAYER["margin"]
    assert et.bonus == TEST_PLAYER["bonus"]


def test_filter_entity_from_dict():
    et = search_filter_entity.SearchFilterEntity.from_dict(TEST_PLAYER)

    assert et.name == TEST_PLAYER["name"]
    assert et.futbin_id == TEST_PLAYER["futbin_id"]
    assert et.margin == TEST_PLAYER["margin"]
    assert et.bonus == TEST_PLAYER["bonus"]


def test_filter_entity_calculate_prices():
    et = search_filter_entity.SearchFilterEntity.from_dict(TEST_PLAYER)

    et.calculate_prices(TEST_MARKET_PRICE)

    assert et.sell_price == TEST_MARKET_PRICE + TEST_PLAYER["bonus"]
    assert et.max_buy_now_price == int(TEST_MARKET_PRICE * 0.95 - TEST_PLAYER["margin"])
    assert isinstance(et.sell_price, int)
    assert isinstance(et.max_buy_now_price, int)


def test_filter_entity_to_dict():
    expected_result = dict(
        name=TEST_PLAYER["name"],
        max_buy_now_price=TEST_MARKET_PRICE * 0.95 - TEST_PLAYER["margin"],
        sell_price=TEST_MARKET_PRICE + TEST_PLAYER["bonus"],
    )

    et = search_filter_entity.SearchFilterEntity.from_dict(TEST_PLAYER)
    et.calculate_prices(TEST_MARKET_PRICE)

    assert et.to_dict() == expected_result
