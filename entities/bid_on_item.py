class BidOnItem:
    def __init__(self, name, bid):
        self.name = name
        self.bid = bid

    @classmethod
    def from_dict(cls, adict):
        return cls(name=adict["name"], bid=adict["bid"],)

    def to_dict(self):
        return {
            "name": self.name,
            "bid": self.bid,
        }
