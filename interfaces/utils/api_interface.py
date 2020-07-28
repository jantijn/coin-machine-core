import requests


class ApiInterface:
    def __init__(self, token, production=False):
        self.token = token
        self.base_url = "" if production else ""
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def get_request(self, url, headers):
        request_url = f"{self.base_url}/{url}"
        return requests.get(url=request_url, headers=headers)

    def post_request(self, url, headers, data):
        request_url = f"{self.base_url}/{url}"
        return requests.post(url=request_url, headers=headers, data=data)
