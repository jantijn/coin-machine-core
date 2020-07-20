import requests


class MarketPriceService:
    def get(self, player_id):
        response = requests.get(self._generate_futbin_request(player_id))
        return self._parse_futbin_response(response, player_id)

    @staticmethod
    def _generate_futbin_request(player_id, game=20):
        return (
            "https://www.futbin.com/"
            + str(game)
            + "/playerPrices?player="
            + str(player_id)
        )

    @staticmethod
    def _parse_futbin_response(response, player_id, platform="ps"):
        return int(
            response.json()[str(player_id)]["prices"][platform]["LCPrice"].replace(
                ",", ""
            )
        )
