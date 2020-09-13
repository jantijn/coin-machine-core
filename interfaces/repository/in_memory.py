from random import random


class Repository:
    def save_purchased_item(self, item):
        pass

    def get_random_items(self, number_of_items):
        items = [
            {"name": "Joe Gomez", "futbin_id": "225100", "margin": 300, "bonus": 100},
            {"name": "Nathan Ake", "futbin_id": "208920", "margin": 300, "bonus": 100},
            {
                "name": "Alex Oxlade-Chamberlain",
                "futbin_id": "198784",
                "margin": 300,
                "bonus": 100,
            },
            {
                "name": "Jesse Lingard",
                "futbin_id": "207494",
                "margin": 300,
                "bonus": 100,
            },
        ]

        return random.sample(items, number_of_items)
