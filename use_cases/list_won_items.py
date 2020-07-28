class ListWonItems:
    def __init__(self, web_app, purchased_items, logger):
        self.web_app = web_app
        self.purchased_items = purchased_items
        self.logger = logger

    def execute(self, search_filters):
        self.logger.log("Listing won items...")
        won_items = self.web_app.list_all_transfer_targets(search_filters)
        for won_item in won_items:
            self.logger.log(f"Listed {won_item.name} for a profit (if sold) of {won_item.profit}")
            self.purchased_items.save_purchased_item(won_item)
