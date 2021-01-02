import random

import requests

from entities.search_filter import SearchFilter


class Repository:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.base_url = "https://coin-machine-repo.herokuapp.com"
        self.headers = None
        self.session = None

    def login(self, username, password):
        url = f"/api/token/"
        data = {"username": username, "password": password}
        response = self._post(url=url, data=data)
        self.access_token = response["access"]
        self.refresh_token = response["refresh"]
        self.headers = {"Authorization": f"Bearer {self.access_token}"}

    def create_session(self):
        url = f"/api/sessions/"
        data = {"type": "mass_bid", "status": "running"}
        response = self._post(url=url, headers=self.headers, data=data)
        self.session = response["id"]
        return response

    def stop_session(self):
        url = f"/api/sessions/{self.session}/stop/"
        return self._post(url=url, headers=self.headers)

    def save_purchased_item(self, item):
        item.calculate_profit()
        data = {
            "session": self.session,
            "item": item.id,
            "purchase_price": int(item.purchase_price),
            "sell_price": int(item.sell_price),
            "profit": int(item.profit),
        }
        url = f"/api/purchased-items/"
        return self._post(url=url, headers=self.headers, data=data)

    def get_random_search_filters(self, number_of_search_filters):
        search_filters = []
        url = f"/api/items/random/"

        for i in range(number_of_search_filters):
            item = self._get(url=url, headers=self.headers)
            search_filter = SearchFilter.from_dict(item)
            search_filters.append(search_filter)

        return search_filters

    def get_item_info(self, name, rating):
        data = {"short_name": name, "rating": rating}
        url = f"/api/items/info/"
        return self._get(url=url, headers=self.headers, data=data)

    def _post(self, url, data={}, headers={}):
        request_url = f"{self.base_url}{url}"
        response = requests.post(url=request_url, headers=headers, data=data).json()
        if "code" in response and response["code"] == "token_not_valid":
            print("expired token")
            self._refresh_token()
            response = self._post(url=url, data=data, headers=self.headers)
        return response

    def _get(self, url, headers, data={}):
        request_url = f"{self.base_url}{url}"
        response = requests.get(url=request_url, headers=headers, data=data).json()
        if "code" in response and response["code"] == "token_not_valid":
            print("expired token")
            self._refresh_token()
            response = self._get(url=url, headers=self.headers, data=data)
        return response

    def _refresh_token(self):
        request_url = f"{self.base_url}/api/refresh/"
        data = {"refresh": self.refresh_token}
        response = requests.post(url=request_url, data=data).json()
        self.access_token = response["access"]
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
