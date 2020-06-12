from mesa import Agent


class Seller(Agent):
    """
    A seller that ...
    """
    def __init__(self, unique_id, goods_left, min_price, model):
        super().__init__(unique_id, model)
        self.goods_left = goods_left
        self.min_price = min_price
        self.buyer = None
        self.is_matched = False

    def __str__(self):
        return "Agent {} (seller) has {} goods left, with min price of {}"\
            .format(self.unique_id, self.goods_left, self.min_price)

    def sell(self):
        self.goods_left -= 1

    def step(self):
        if self.is_matched:
            self.sell()


class Buyer(Agent):
    """
    A buyer that ...
    """
    def __init__(self, unique_id, money_left, max_price, model):
        super().__init__(unique_id, model)
        self.money_left = money_left
        self.max_price = max_price
        self.seller = None
        self.is_matched = False

    def __str__(self):
        return "Agent {} (buyer) has ${} left, with max price of {}"\
            .format(self.unique_id, self.money_left, self.max_price)

    def buy(self):
        cost = (self.max_price + self.seller.min_price) / 2
        self.money_left -= cost

    def step(self):
        if self.is_matched:
            self.buy()







