import requests


class MarketDataInterface:

    def get_market_price(self, player_id, platform="ps"):
        response = requests.get(self._generate_futbin_request(player_id))
        return self._parse_futbin_response(response, player_id, platform)

    @staticmethod
    def _generate_futbin_request(player_id, game=20):
        return f"https://www.futbin.com/{game}/playerPrices?player={player_id}"

    @staticmethod
    def _parse_futbin_response(response, player_id, platform):
        price_string = response.json()[str(player_id)]["prices"][platform]["LCPrice"]
        return int(price_string.replace(",", ""))
