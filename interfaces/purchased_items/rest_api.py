from interfaces.utils.api_interface import ApiInterface


class PurchasedItemInterface(ApiInterface):
    def __init__(self, token, session, production=False):
        super().__init__(token, production)
        self.session = session

    def save_purchased_item(self, item):
        url = f"/mass_bidder/session/{self.session}/purchased-items/"
        return self.post_request(url, data=item)
