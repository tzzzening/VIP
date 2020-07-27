from mesa.time import SimultaneousActivation
from mesa import Agent
from abm_buyer_seller.agents import WasteAgent
from abm_buyer_seller.agents import Buyer, Seller
from abm_buyer_seller.enums import CapacityPlanningStrategies
import bisect
import random
from statistics import mean
import numpy as np


class SimultaneousActivationMoneyModel(SimultaneousActivation):
    """
    SimultaneousActivation class with added lists to store buyers and sellers separately.
    """

    total_waste_produced = 0
    total_waste_traded = 0

    total_cost_without_trading_seller = 0  # cost incurred without trading waste, ie all waste is disposed of
    total_cost_with_trading_seller = 0
    total_cost_without_trading_buyer = 0  # cost incurred without trading waste, ie all waste is disposed of
    total_cost_with_trading_buyer = 0
    # random.seed(1)

    def __init__(self, model) -> None:
        super().__init__(model)
        self.sellers = []
        self.buyers = []
        self.steps = 1
        # print('TIME INIT')
        random.seed(1)

    def __str__(self) -> str:
        output = ""
        for i in self.sellers:
            output += (i[2].__str__() + "\n")  # not sure if should change to get_seller_from_list
        for i in self.buyers:
            output += (i[2].__str__() + "\n")
        return output

    def add(self, agent: WasteAgent) -> None:
        self._agents[agent.unique_id] = agent
        if isinstance(agent, Seller):
            bisect.insort(self.sellers, (agent.min_price, agent.unique_id, agent))
        elif isinstance(agent, Buyer):
            bisect.insort(self.buyers, (agent.max_price, agent.unique_id, agent))
        else:
            raise Exception  # specify exception later, not sure about python exceptions

    def step(self) -> None:
        """
        Executes the step of all agents.
        After which, updates the class variables for recycling rate and cost savings calculation.
        Finally, executes the advance of all agents.
        """
        # print('yoyoo')
        # print(self.__str__())
        # self.match_agents()
        # for agent in self.agent_buffer(shuffled=False):
        #     # maybe can come back and check this buffer thing and try to change it to a WasteAgent
        #     agent.step()
        #     if isinstance(agent, Seller):
        #         self.total_waste_produced += agent.waste_left
        #         self.total_cost_without_trading_seller += \
        #             agent.waste_left * agent.cost_per_unit_waste_disposed
        #         if agent.is_matched:
        #             self.set_trade_quantity(agent)
        #
        # for agent in self.agent_buffer(shuffled=False):
        #     agent.advance()
        # here
        daily_demand = random.randint(5, 10)  # assume that all agents have the same demand
        for i in range(len(self.sellers)):
        # for i in range(2):
            seller = self.get_seller_from_list(i)
            seller.step()
            self.update_variables_seller(seller, daily_demand)

        for i in range(len(self.buyers)):
        # for i in range(2):
            buyer = self.get_buyer_from_list(i)
            buyer.step()
            self.update_variables_buyer(buyer, daily_demand)

        for agent in self.agent_buffer(shuffled=False):
            # print(agent.daily_demand)
            # print(agent.capacity_planning_strategy)
            agent.advance()
            # print(agent.demand_list)
            print('cap list', agent.capacity_list)
            print('pro list', agent.production_list)
            # print(agent.capacity)
            if self.steps % 28 == 0:
                self.plan_capacity(agent)
            elif self.steps % 28 == agent.days_taken_to_increase_capacity and self.steps > 28:
                agent.production_capacity = agent.new_production_capacity

        self.steps += 1
        self.time += 1

    def set_trade_quantity(self, seller) -> None:
        buyer = seller.buyer
        seller_quantity = seller.waste_left
        buyer_quantity = buyer.waste_treatment_capacity
        trade_quantity = min(seller_quantity, buyer_quantity)
        seller.trade_quantity = trade_quantity
        buyer.trade_quantity = trade_quantity
        # buyer.total_input = buyer.new_input + trade_quantity
        self.total_waste_traded += trade_quantity
        return

    def get_seller_from_list(self, index) -> Seller:
        return self.sellers[index][2]

    def get_buyer_from_list(self, index) -> Buyer:
        return self.buyers[index][2]

    def update_variables_seller(self, seller, daily_demand) -> None:
        seller.weekly_demand = daily_demand
        self.total_waste_produced += seller.waste_left
        self.total_cost_without_trading_seller += \
            seller.waste_left * seller.cost_per_unit_waste_disposed + \
            seller.maintenance_cost_per_capacity * seller.production_capacity

        self.total_cost_with_trading_seller += \
            seller.maintenance_cost_per_capacity * seller.production_capacity

        if seller.is_matched:
            self.set_trade_quantity(seller)
            cost = (seller.waste_left - seller.trade_quantity) * \
                seller.cost_per_unit_waste_disposed - \
                seller.trade_quantity * seller.trade_cost
            self.total_cost_with_trading_seller += cost
        else:
            self.total_cost_with_trading_seller += \
                seller.waste_left * seller.cost_per_unit_waste_disposed
        return

    def update_variables_buyer(self, buyer, daily_demand) -> None:
        buyer.weekly_demand = daily_demand
        self.total_cost_without_trading_buyer += \
            buyer.new_input * buyer.cost_per_new_input + \
            buyer.maintenance_cost_per_capacity * buyer.total_capacity
            # buyer.maintenance_cost_per_capacity * buyer.weekly_capacity

        # self.total_cost_with_trading_buyer += buyer.maintenance_cost_per_capacity * buyer.weekly_capacity
        self.total_cost_with_trading_buyer += buyer.maintenance_cost_per_capacity * buyer.total_capacity

        if buyer.is_matched:
            cost = buyer.new_input * buyer.cost_per_new_input + \
                   buyer.trade_quantity * buyer.trade_cost
            self.total_cost_with_trading_buyer += cost
        else:
            self.total_cost_with_trading_buyer += \
                buyer.new_input * buyer.cost_per_new_input
        return

    def plan_capacity(self, agent: WasteAgent) -> None:
        if self.steps % 28 != 0:  # take 28 weeks of data to come out with the forecast
            return
        x_values = np.array(list(range(1, 29)), dtype=np.float64)
        y_values = np.array(agent.demand_list, dtype=np.float64)
        m, c = self.best_fit_slope_and_intercept(x_values, y_values)
        print('gradient and y-intercept', m, c)
        if agent.capacity_planning_strategy is CapacityPlanningStrategies.lead:
            print('lead')
            agent.new_production_capacity = int(56 * m + c)  # change magic numbers later
        elif agent.capacity_planning_strategy is CapacityPlanningStrategies.match:
            print('match')
            agent.new_production_capacity = int(42 * m + c)
        elif agent.capacity_planning_strategy is CapacityPlanningStrategies.lag:
            print('lag')
            agent.new_production_capacity = int(28 * m + c)
        else:
            raise Exception

    @staticmethod
    def best_fit_slope_and_intercept(x_values, y_values):
        m = (((mean(x_values) * mean(y_values)) - mean(x_values * y_values)) /
             ((mean(x_values) * mean(x_values)) - mean(x_values * x_values)))
        c = mean(y_values) - m * mean(x_values)
        return m, c





















