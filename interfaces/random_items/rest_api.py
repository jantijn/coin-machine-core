from interfaces.utils.api_interface import ApiInterface


class RandomItemsInterface(ApiInterface):
    def __init__(self, token, session, production=False):
        super().__init__(token, production)
        self.session = session

    def get(self, number_of_items):
        random_items = []
        while len(random_items) < number_of_items:
            random_item = self._get_random_item()
            if random_item not in random_items:
                random_items.append(random_item)

    def _get_random_item(self):
        url = f"/items/random"
        return self.get_request(url)
