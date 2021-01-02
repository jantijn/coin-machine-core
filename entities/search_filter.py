class SearchFilter:
    def __init__(self, repo_id, name, market_price):
        self.id = repo_id
        self.name = name
        self.market_price = market_price
        self.buy_price = None
        self.sell_price = None

    @classmethod
    def from_dict(cls, adict):
        return cls(
            repo_id=adict["name"],
            name=adict["short_name"],
            market_price=adict["last_market_price"],
        )

    def calculate_prices(self, margin, bonus):
        ea_tax = 0.05
        self.buy_price = int(
            round((self.market_price * (1 - ea_tax) - margin) / 100, 0) * 100
        )
        self.sell_price = self.market_price + bonus

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "max_buy_now_price": self.buy_price,
            "sell_price": self.sell_price,
        }
