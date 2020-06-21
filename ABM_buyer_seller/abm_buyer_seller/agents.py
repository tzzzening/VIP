from mesa import Agent


class Seller(Agent):
    """
    A seller that ...
    """
    def __init__(self, unique_id, goods_left, min_price, model) -> None:
        super().__init__(unique_id, model)
        self.goods_left = goods_left
        self.min_price = min_price
        self.buyer = None
        self.is_matched = False
        self.trade_quantity = None

    def __str__(self) -> str:
        output = "Agent {} (seller) has {} goods left, with min price of {}. "\
            .format(self.unique_id, self.goods_left, self.min_price)
        if self.is_matched:
            output += "Sold to buyer {}.".format(self.buyer.unique_id)
        return output

    def sell(self) -> None:
        self.goods_left = self.goods_left - self.trade_quantity

    def step(self) -> None:
        if self.is_matched:
            self.sell()


class Buyer(Agent):
    """
    A buyer that ...
    """
    def __init__(self, unique_id, money_left, max_price, model) -> None:
        super().__init__(unique_id, model)
        self.money_left = money_left
        self.max_price = max_price
        self.seller = None
        self.is_matched = False
        self.cost = None
        self.trade_quantity = None

    def __str__(self) -> str:
        output = "Agent {} (buyer) has ${} left, with max price of {}. "\
            .format(self.unique_id, self.money_left, self.max_price)
        if self.is_matched:
            output += "Bought from seller {}.".format(self.seller.unique_id)
        return output

    def buy(self) -> None:
        self.money_left = self.money_left - (self.trade_quantity * self.cost)

    def step(self) -> None:
        if self.is_matched:
            self.buy()







