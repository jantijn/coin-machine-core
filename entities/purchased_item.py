class PurchasedItem:
    def __init__(self, name, purchase_price, sell_price):
        self.name = name
        self.purchase_price = purchase_price
        self.sell_price = sell_price
        self.profit = self._calculate_profit(purchase_price, sell_price)

    @classmethod
    def from_dict(cls, adict):
        return cls(
            name=adict["name"],
            purchase_price=adict["purchase_price"],
            sell_price=adict["sell_price"],
        )

    def to_dict(self):
        return {
            "name": self.name,
            "purchase_price": self.purchase_price,
            "sell_price": self.sell_price,
            "profit": self.profit,
        }

    @staticmethod
    def _calculate_profit(purchase_price, sell_price):
        profit = sell_price * 0.95 - purchase_price
        return round(profit / 100, 0) * 100
