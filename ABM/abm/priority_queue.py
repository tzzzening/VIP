from queue import PriorityQueue


class CustomPriorityQueue(PriorityQueue):
    def __init__(self):
        super().__init__()

    def peek(self):
        return self.queue[0]


class SellerPriorityQueue(CustomPriorityQueue):
    def __init__(self):
        super().__init__()

    def put_in_queue(self, seller):
        self.put((seller.min_price, seller.unique_id, seller))


class BuyerPriorityQueue(CustomPriorityQueue):
    def __init__(self):
        super().__init__()

    def put_in_queue(self, buyer):
        self.put((buyer.max_price, buyer.unique_id, buyer))








