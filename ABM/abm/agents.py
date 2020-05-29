from mesa import Agent


class Seller(Agent):
    """
    A seller that ...
    """
    def __init__(self, unique_id, num_goods, min_price, model):
        super().__init__(unique_id, model)
        self.num_of_goods = num_goods
        self.min_price = min_price

    def __str__(self):
        return "Seller {} has {} goods left.".format(self.unique_id, self.num_of_goods)

    def sell(self):
        self.num_of_goods -= 1

    def step(self):
        print("seller step")

    # def advance(self):
    #     print("seller advance")


class Buyer(Agent):
    """
    A buyer that ...
    """
    def __init__(self, unique_id, amt_money, max_price, model):
        super().__init__(unique_id, model)
        self.money = amt_money
        self.max_price = max_price

    def __str__(self):
        return "Buyer {} has ${} left.".format(self.unique_id, self.money)

    def buy(self, cost):
        self.money -= cost

    def step(self):
        print("buyer step")

    # def advance(self):
    #     print("buyer advance")


