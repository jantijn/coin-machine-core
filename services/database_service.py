import time

import requests


class DatabaseService:
    def __init__(self, session_hash, token):
        self._session_hash = session_hash
        self._token = token

    def save(self, name, purchase_price, sell_price, profit):
        url = 'http://127.0.0.1:8000/sniper/session/' + str(self._session_hash) + '/purchased-players/'
        data = {
            'name': name,
            'purchase_price': int(purchase_price),
            'sell_price': int(sell_price),
            'profit': int(profit),
        }
        headers = {"Authorization": "Bearer " + str(self._token)}
        return requests.post(url, data = data, headers = headers)
