class SearchResultEntity:
    def __init__(self, name, rating, buy_now_price):
        self.name = name
        self.rating = rating
        self.buy_now_price = buy_now_price

    @classmethod
    def from_dict(cls, adict):
        return cls(name=adict["name"], rating=adict["rating"], buy_now_price=adict["buy_now_price"])

    def to_dict(self):
        return {
            "name": self.name,
            "rating": self.rating,
            "buy_now_price": self.buy_now_price
        }
