class PurchasedItemEntity:
    def __init__(self):
        self.id = None
        self.name = None
        self.purchase_price = None
        self.sell_price = None
        self.rating = None
        self.profit = None

    def list(self, sell_price):
        pass

    def to_dict(self):
        self.calculate_profit()
        return {
            "id": self.id,
            "name": self.name,
            "rating": self.rating,
            "purchase_price": self.purchase_price,
            "sell_price": self.sell_price,
            "profit": self.profit,
        }

    def calculate_profit(self):
        profit = self.sell_price * 0.95 - self.purchase_price
        self.profit = round(profit / 100, 0) * 100
