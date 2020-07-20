import time
import requests


class PlayerService:
    # def __init__(self, session_hash, token):
    #     self._session_hash = session_hash
    #     self._token = token

    def get(self):
        return [
            {'name': 'Joe Gomez', 'futbin_id': '225100', 'margin': 300, 'bonus': 100},
            {'name': 'Nathan Ake', 'futbin_id': '208920', 'margin': 300, 'bonus': 100},
        ]

        # return {'name': 'TANGUY NDOMBELE', 'futbin_id': '235569', 'margin': 300, 'bonus': 100}
    #     players = []
    #     while len(players) == 0:
    #         time.sleep(0.5)
    #         players = self._get_player()
    #     return players[0]

    # def _get_player(self):
    #     response = requests.get('http://127.0.0.1:8000/sniper/session/' + str(self._session_hash) + '/player/', 
    #         headers={"Authorization": "Bearer " + str(self._token)}
    #     )
    #     return response.json()
