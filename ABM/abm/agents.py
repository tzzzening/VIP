from mesa import Agent


class MoneyAgent(Agent):  # may not need this
    """An agent in the MoneyModel."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


class Seller(MoneyAgent):
    def __init__(self, unique_id, num_of_goods, min_price, model):
        super().__init__(unique_id, model)
        self.num_of_goods = num_of_goods
        self.min_price = min_price

    def __str__(self):
        return "Seller {} has {} goods left.".format(self.unique_id, self.num_of_goods)

    def sell(self):
        self.num_of_goods -= 1


class Buyer(MoneyAgent):
    def __init__(self, unique_id, money, max_price, model):
        super().__init__(unique_id, model)
        self.money = money
        self.max_price = max_price

    def __str__(self):
        return "Buyer {} has ${} left.".format(self.unique_id, self.money)

    def buy(self, cost):
        self.money -= cost
