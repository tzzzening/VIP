from mesa import Agent
from abm_buyer_seller.enums import CapacityPlanningStrategies


class WasteAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.is_matched = False
        self.trade_quantity = 0
        # self.cost_to_change_capacity = 5  # assume that it is the same cost to increase or decrease capacity
        self.days_taken_to_increase_capacity = 7
        self.weekly_demand = 0
        self.demand_list = []
        self.capacity_list = []  # temporary
        self.production_list = []  # temporary
        self.price_list = []  # temporary
        self.capacity_planning_strategy = None
        self.day_capacity_changes = 0
        self.new_production_capacity = 0
        self.maintenance_cost_per_capacity = 1
        self.weekly_production = 0
        self.production_capacity = 0
        self.profit_per_good = 50

    def edit_demand_list(self) -> None:
        self.demand_list.append(self.weekly_demand)
        self.capacity_list.append(self.production_capacity)  # temp
        self.production_list.append(self.weekly_production)  # temp
        if isinstance(self, Seller):
            self.price_list.append(self.min_price)  # temp
        elif isinstance(self, Buyer):
            self.price_list.append(self.max_price)  # temp
        if len(self.demand_list) > 28:  # 28 is the number to plot the demand forecast
            del self.demand_list[0]
            del self.capacity_list[0]  # temp
            del self.production_list[0]  # temp
            del self.price_list[0]  # temp


class Seller(WasteAgent):
    """
    A seller that ...
    """
    def __init__(self, unique_id, min_price, production_capacity, model) -> None:
        super().__init__(unique_id, model)
        self.min_price = min_price
        self.production_capacity = production_capacity
        self.buyer = None
        self.waste_left = 0
        self.cost_per_unit_waste_disposed = 15
        self.trade_cost = 0
        self.capacity_planning_strategy = CapacityPlanningStrategies.lead
        self.waste_generated_per_good = 2

    def __str__(self) -> str:
        output = "Agent {} (seller) has {} waste produced, with min price of {}. "\
            .format(self.unique_id, self.waste_left, self.min_price)
        if self.is_matched:
            output += "Sold to buyer {}.".format(self.buyer.unique_id)
        return output

    def sell(self) -> None:
        self.waste_left -= self.trade_quantity

    def step(self) -> None:
        """
        Generate production and waste for the week.
        """
        self.weekly_production = self.production_capacity
        self.waste_left = self.waste_generated_per_good * self.weekly_production

    def advance(self) -> None:
        if self.is_matched:
            self.sell()
        self.edit_demand_list()


class Buyer(WasteAgent):
    """
    A buyer that ...
    """
    def __init__(self, unique_id, waste_treatment_capacity, max_price, production_capacity, model) -> None:
        super().__init__(unique_id, model)
        self.waste_treatment_capacity = waste_treatment_capacity
        self.max_price = max_price
        self.seller = None
        self.trade_cost = None
        self.waste_treatment_capacity_left = 0
        self.cost_per_new_input = 20  # but there will come a point when the waste is more expensive
        self.new_input = 150
        self.input_per_good = 1
        self.production_capacity = production_capacity
        self.capacity_planning_strategy = CapacityPlanningStrategies.lag

    def __str__(self) -> str:
        output = "Agent {} (buyer) has capacity of {}, with max price of {}. "\
            .format(self.unique_id, self.waste_treatment_capacity_left, self.max_price)
        if self.is_matched:
            output += "Bought from seller {}.".format(self.seller.unique_id)
        return output

    def buy(self) -> None:
        self.waste_treatment_capacity_left -= self.trade_quantity

    def step(self) -> None:
        """
        Update waste treatment capacity and generate production.
        """
        self.waste_treatment_capacity_left = self.waste_treatment_capacity
        self.weekly_production = min(self.production_capacity, self.total_input // self.input_per_good)

    def advance(self) -> None:
        if self.is_matched:
            self.buy()
        self.edit_demand_list()

    @property
    def total_input(self):
        if self.is_matched:
            return self.new_input + self.trade_quantity
        else:
            return self.new_input

    @property
    def total_capacity(self):
        return self.production_capacity + self.waste_treatment_capacity






