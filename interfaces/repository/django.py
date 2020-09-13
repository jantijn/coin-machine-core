import requests


class Repository:
    def __init__(self, token, session):
        self.token = token
        self.base_url = ""
        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.session = session

    def save_purchased_item(self, item):
        url = f"/session/{self.session}/purchased-items/"
        return self._post(url=url, headers=self.headers, data=item)

    def _post(self, url, headers, data):
        request_url = f"{self.base_url}/{url}"
        return requests.post(url=request_url, headers=headers, data=data)

    def get_random_items(self, number_of_items):
        random_items = []
        while len(random_items) < number_of_items:
            random_item = self._get_random_item()
            if random_item not in random_items:
                random_items.append(random_item)
        return random_items

    def _get_random_item(self):
        url = f"/items/random"
        return self._get(url=url, headers=self.headers)

    def _get(self, url, headers):
        request_url = f"{self.base_url}/{url}"
        return requests.get(url=request_url, headers=headers)
