from mesa import Agent
import random
from abm_buyer_seller.enums import CapacityPlanningStrategies


class WasteAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.is_matched = False
        self.trade_quantity = 0
        self.cost_to_change_capacity = 5  # assume that it is the same cost to increase or decrease capacity
        self.days_taken_to_increase_capacity = 7
        self.weekly_demand = 0
        self.demand_list = []
        self.capacity_list = []  # temporary
        self.production_list = [] # temporary
        self.capacity_planning_strategy = None
        self.day_capacity_changes = 0
        self.new_capacity = 0
        self.maintenance_cost_per_capacity = 1
        self.weekly_production = 0

    def edit_demand_list(self) -> None:
        self.demand_list.append(self.weekly_demand)
        self.capacity_list.append(self.capacity)  # temp
        self.production_list.append(self.weekly_production)  # temp
        if len(self.demand_list) > 28:  # 28 is the number to plot the demand forecast
            del self.demand_list[0]
            del self.capacity_list[0]  # temp
            del self.production_list[0]


class Seller(WasteAgent):
    """
    A seller that ...
    """
    def __init__(self, unique_id, weekly_waste_produced, min_price, capacity, model) -> None:
        super().__init__(unique_id, model)
        self.weekly_waste_produced = weekly_waste_produced
        self.min_price = min_price
        self.capacity = capacity
        self.buyer = None
        self.waste_left = 0
        self.cost_per_unit_waste_disposed = 4
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
        self.weekly_production = self.capacity
        self.waste_left = self.waste_generated_per_good * self.weekly_production
        # self.waste_left = random.randint((self.weekly_waste_produced - 1), (self.weekly_waste_produced + 1))
        # self.waste_left = 6

    def advance(self) -> None:
        # print('seller {} has {} waste left'.format(self.unique_id, self.waste_left))
        if self.is_matched:
            self.sell()
        # print('seller {} has {} waste left'.format(self.unique_id, self.waste_left))
        self.edit_demand_list()


class Buyer(WasteAgent):
    """
    A buyer that ...
    """
    def __init__(self, unique_id, weekly_capacity, max_price, capacity, model) -> None:
        super().__init__(unique_id, model)
        self.weekly_capacity = weekly_capacity  # for waste treatment?
        self.max_price = max_price
        self.seller = None
        self.trade_cost = None
        self.capacity_left = 0
        self.cost_per_new_input = 10
        # self.input = 10
        self.new_input = 2  # change later
        # self.total_input = 0
        self.input_per_good = 1
        self.capacity = capacity  # for goods
        self.capacity_planning_strategy = CapacityPlanningStrategies.match

    def __str__(self) -> str:
        output = "Agent {} (buyer) has capacity of {}, with max price of {}. "\
            .format(self.unique_id, self.capacity_left, self.max_price)
        if self.is_matched:
            output += "Bought from seller {}.".format(self.seller.unique_id)
        return output

    def buy(self) -> None:
        self.capacity_left -= self.trade_quantity

    def step(self) -> None:
        """

        :return:
        """
        self.capacity_left = self.weekly_capacity  # this is wrong, capacity left is refering to waste, weekly capacity is refering to production
        self.weekly_production = min(self.capacity, self.total_input / self.input_per_good)

    def advance(self) -> None:
        # print('buyer {} has {} capacity left'.format(self.unique_id, self.capacity_left))
        if self.is_matched:
            self.buy()
        # print('buyer {} has {} capacity left'.format(self.unique_id, self.capacity_left))
        self.edit_demand_list()

    @property
    def total_input(self):
        if self.is_matched:
            return self.new_input + self.trade_quantity
        else:
            return self.new_input






