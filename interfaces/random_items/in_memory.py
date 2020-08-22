import random


class RandomItemsInterface:
    def __init__(self):
        self.items = [
            {"name": "Joe Gomez", "futbin_id": "225100", "margin": 300, "bonus": 100},
            {"name": "Nathan Ake", "futbin_id": "208920", "margin": 300, "bonus": 100},
            {"name": "Alex Oxlade-Chamberlain", "futbin_id": "198784", "margin": 300, "bonus": 100},
            {"name": "Jesse Lingard", "futbin_id": "207494", "margin": 300, "bonus": 100},
        ]

    def get(self, number_of_items):
        return random.sample(self.items, number_of_items)
