class SearchFilter:
    def __init__(self, name, margin=100, bonus=0):
        self.name = name
        self.margin = margin
        self.bonus = bonus
        self.buy_price = None
        self.sell_price = None

    @classmethod
    def from_dict(cls, adict):
        return cls(name=adict["name"], margin=adict["margin"], bonus=adict["bonus"],)

    def calculate_prices(self, market_price):
        self.buy_price = _calculate_max_buy_now_price(
            market_price=market_price, margin=self.margin
        )
        self.sell_price = _calculate_sell_price(
            market_price=market_price, bonus=self.bonus
        )

    def to_dict(self):
        return {
            "name": self.name,
            "max_buy_now_price": self.buy_price,
            "sell_price": self.sell_price,
        }


def _calculate_sell_price(market_price, bonus):
    return market_price + bonus


def _calculate_max_buy_now_price(market_price, margin):
    ea_tax = 0.05
    return int(round((market_price * (1 - ea_tax) - margin) / 100, 0) * 100)
