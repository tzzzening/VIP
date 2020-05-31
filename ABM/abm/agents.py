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

    def __str__(self):
        return "Seller {} has {} goods left.".format(self.unique_id, self.goods_left)

    def sell(self):
        self.goods_left -= 1

    def step(self):
        print("seller step")
        # if self.goods_left > 0 and self.buyer.money_left >= self.min_price:
        #     if self.min_price <= self.buyer.max_price:
        #         self.sell()
        # okay no it won't work. i need a way to check if it's supposed to sell in
        # the advance method

    # while seller.num_of_goods > 0 and buyer.money >= seller.min_price:
    #     if seller.min_price <= buyer.max_price:
    #         seller.sell()
    #         buyer.buy((seller.min_price + buyer.max_price) / 2)

    # def advance(self):
    #     print("seller advance")


class Buyer(Agent):
    """
    A buyer that ...
    """
    def __init__(self, unique_id, money_left, max_price, model):
        super().__init__(unique_id, model)
        self.money_left = money_left
        self.max_price = max_price
        self.seller = None

    def __str__(self):
        return "Buyer {} has ${} left.".format(self.unique_id, self.money_left)

    def buy(self, cost):
        self.money_left -= cost

    def step(self):
        print("buyer step")

    # def advance(self):
    #     print("buyer advance")


