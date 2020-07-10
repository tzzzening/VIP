from mesa import Agent


class WasteAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.is_matched = False
        self.trade_quantity = 0


class Seller(WasteAgent):
    """
    A seller that ...
    """
    def __init__(self, unique_id, monthly_waste_produced, min_price, model) -> None:
        super().__init__(unique_id, model)
        self.monthly_waste_produced = monthly_waste_produced
        self.min_price = min_price
        self.buyer = None
        self.waste_left = monthly_waste_produced

    def __str__(self) -> str:
        output = "Agent {} (seller) has {} waste produced, with min price of {}. "\
            .format(self.unique_id, self.waste_left, self.min_price)
        if self.is_matched:
            output += "Sold to buyer {}.".format(self.buyer.unique_id)
        return output

    def sell(self) -> None:
        self.waste_left -= self.trade_quantity

    def step(self) -> None:
        self.waste_left = self.monthly_waste_produced

    def advance(self) -> None:
        if self.is_matched:
            self.sell()


class Buyer(WasteAgent):
    """
    A buyer that ...
    """
    def __init__(self, unique_id, monthly_capacity, max_price, model) -> None:
        super().__init__(unique_id, model)
        self.monthly_capacity = monthly_capacity
        self.max_price = max_price
        self.seller = None
        self.cost = None  # i think this one also don't need. okay maybe not
        self.capacity_left = monthly_capacity

    def __str__(self) -> str:
        output = "Agent {} (buyer) has capacity of {}, with max price of {}. "\
            .format(self.unique_id, self.capacity_left, self.max_price)
        if self.is_matched:
            output += "Bought from seller {}.".format(self.seller.unique_id)
        return output

    def buy(self) -> None:
        self.capacity_left -= self.trade_quantity

    def step(self) -> None:
        self.capacity_left = self.monthly_capacity

    def advance(self) -> None:
        if self.is_matched:
            self.buy()






