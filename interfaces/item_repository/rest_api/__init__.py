import requests


class RepositoryInterface:
    def __init__(self, token, session, production=False):
        self.token = token
        self.session = session
        self.base_url = '' if production else ''

    def get_random_item(self):
        url = f'{self.base_url}/items/random/'
        headers = self._get_headers()
        return requests.get(url, headers = headers)

    def save_purchased_item(self, item):
        url = f'{self.base_url}/mass_bidder/session/{self.session}/purchased-items/'
        headers = self._get_headers()
        return requests.post(url, data = item, headers = headers)

    def _get_headers(self):
        return {'Authorization': f'Bearer {self.token}'}
