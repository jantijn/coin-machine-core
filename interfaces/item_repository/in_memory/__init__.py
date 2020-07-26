from random import random


class RepositoryInterface:
    def get_random_item(self):
        items = [
            {'name': 'Joe Gomez', 'futbin_id': '225100', 'margin': 300, 'bonus': 100},
            {'name': 'Nathan Ake', 'futbin_id': '208920', 'margin': 300, 'bonus': 100},
        ]
        return random.choice(items)

    def save_purchased_item(self, item):
        pass
