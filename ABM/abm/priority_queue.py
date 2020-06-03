from queue import PriorityQueue


class SellerPriorityQueue(PriorityQueue):
    def __init__(self):
        super().__init__()

    def put_in_queue(self, seller):
        self.put((seller.min_price, seller.unique_id, seller))


class BuyerPriorityQueue(PriorityQueue):
    def __init__(self):
        super().__init__()

    def put_in_queue(self, buyer):
        self.put((buyer.max_price, buyer.unique_id, buyer))








