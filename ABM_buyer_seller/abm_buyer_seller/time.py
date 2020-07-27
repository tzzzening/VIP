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
        random.seed(4)

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
        Executes the step of all agents
        and updates the class variables for recycling rate and cost savings calculation.
        Finally, executes the advance of all agents.
        """
        if self.steps == 1:
            self.match_agents()  # shift to every month
            print(self)
        # daily_demand = random.randint(5, 10)  # assume that all agents have the same demand
        average_daily_demand = int(self.steps * 0.01 + 5)  # steps * gradient + y-intercept
        daily_demand = random.randint(average_daily_demand - 2, average_daily_demand + 2)
        for i in range(self.seller_num):
            seller = self.get_seller_from_list(i)
            seller.step()
            self.update_variables_seller(seller, daily_demand)

        for i in range(self.buyer_num):
            buyer = self.get_buyer_from_list(i)
            buyer.step()
            self.update_variables_buyer(buyer, daily_demand)

        if self.steps % 28 == 0:
            self.sellers = []
            self.buyers = []

        for agent in self.agent_buffer(shuffled=False):
            agent.advance()
            print(agent.demand_list)
            print('cap list', agent.capacity_list)
            # print('pro list', agent.production_list)
            # print('price list', agent.price_list)
            # print(agent.capacity)
            if self.steps % 28 == 0:
                self.plan_capacity(agent)
                self.change_price(agent)
            elif self.steps % 28 == agent.days_taken_to_increase_capacity and self.steps > 28:
                agent.production_capacity = agent.new_production_capacity

        if self.steps % 28 == 0:
            print(self)
            self.initialise_agents()
            self.match_agents()
        # if self.steps == 29:
        #     print(self)

        self.steps += 1
        self.time += 1

    def match_agents(self) -> None:
        """
        Match agents according to minimum price of the seller and the maximum price of the buyer.
        """
        i = 0
        j = 0
        while True:
            print(i, j)
            seller = self.get_seller_from_list(i)
            buyer = self.get_buyer_from_list(j)
            if seller.min_price > buyer.max_price:
                print('{} rejected'.format(j))
                if j == self.buyer_num - 1:
                    break
                j += 1
                continue

            self.prepare_trade(seller, buyer)
            print('{} match {}'.format(i, j))
            if i == (self.seller_num - 1) or j == (self.buyer_num - 1):
                break
            i += 1
            j += 1
        return

    @staticmethod
    def prepare_trade(seller, buyer) -> None:
        """
        Update the trading partners and the cost per unit waste of each agent.
        :param seller:
        :param buyer:
        """

        seller.buyer = buyer
        buyer.seller = seller
        seller.is_matched = True
        buyer.is_matched = True

        cost = (seller.min_price + buyer.max_price) / 2
        seller.trade_cost = cost
        buyer.trade_cost = cost
        return

    def set_trade_quantity(self, seller) -> None:
        """
        Decides on the amount of waste to trade.
        :param seller:
        :return:
        """
        buyer = seller.buyer
        seller_quantity = seller.waste_left
        buyer_quantity = buyer.waste_treatment_capacity
        trade_quantity = min(seller_quantity, buyer_quantity)
        seller.trade_quantity = trade_quantity
        buyer.trade_quantity = trade_quantity
        self.total_waste_traded += trade_quantity
        return

    def get_seller_from_list(self, index) -> Seller:
        """
        Returns seller from list of tuples.
        """
        return self.sellers[index][2]

    def get_buyer_from_list(self, index) -> Buyer:
        """
        Returns buyer from list of tuples.
        """
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
    def best_fit_slope_and_intercept(x_values, y_values) -> tuple:
        m = (((mean(x_values) * mean(y_values)) - mean(x_values * y_values)) /
             ((mean(x_values) * mean(x_values)) - mean(x_values * x_values)))
        c = mean(y_values) - m * mean(x_values)
        return m, c

    def change_price(self, agent) -> None:
        percentage_change = agent.new_production_capacity / agent.production_capacity
        if isinstance(agent, Seller):
            new_price = int(agent.min_price * percentage_change)
            agent.min_price = random.randint(new_price - 1, new_price + 1)
        elif isinstance(agent, Buyer):
            new_price = int(agent.max_price * percentage_change)
            agent.max_price = random.randint(new_price - 1, new_price + 1)
        self.add(agent)

    @property
    def seller_num(self) -> int:
        return len(self.sellers)

    @property
    def buyer_num(self) -> int:
        return len(self.buyers)

    def initialise_agents(self) -> None:
        for agent in self.agent_buffer(shuffled=False):
            agent.is_matched = False
        return






















