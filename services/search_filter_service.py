import requests

from entities.search_filter_entity import SearchFilterEntity


def get_market_price_from_futbin(player_id):
    response = requests.get(generate_futbin_request(player_id))
    return parse_market_price_from_response(response, player_id)


def generate_futbin_request(player_id, game=20):
    return (
            "https://www.futbin.com/"
            + str(game)
            + "/playerPrices?player="
            + str(player_id)
    )


def parse_market_price_from_response(response, player_id, platform="ps"):
    return int(
        response.json()[str(player_id)]["prices"][platform]["LCPrice"].replace(
            ",", ""
        )
    )


class SearchFilterService:
    def get_random_search_filters(self, number):
        items = self.get_random_items()
        search_filters = []
        for item in items:
            search_filter = SearchFilterEntity.from_dict(item)
            search_filter.calculate_prices(get_market_price_from_futbin(search_filter.futbin_id))
            search_filters.append(search_filter)
        return search_filters

    def get_random_items(self):
        return [
            {'name': 'Joe Gomez', 'futbin_id': '225100', 'margin': 300, 'bonus': 100},
            {'name': 'Nathan Ake', 'futbin_id': '208920', 'margin': 300, 'bonus': 100},
        ]