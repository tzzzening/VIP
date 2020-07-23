from mesa.time import SimultaneousActivation
from mesa import Agent
from abm_buyer_seller.agents import WasteAgent
from abm_buyer_seller.agents import Buyer, Seller
from abm_buyer_seller.enums import CapacityPlanningStrategies
import bisect
import random


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
            # print(agent.demand_list)
            print(agent.capacity_planning_strategy)
            agent.advance()

            self.plan_capacity(agent)

        self.steps += 1
        self.time += 1

    def set_trade_quantity(self, seller) -> None:
        buyer = seller.buyer
        seller_quantity = seller.waste_left
        buyer_quantity = buyer.monthly_capacity
        trade_quantity = min(seller_quantity, buyer_quantity)
        seller.trade_quantity = trade_quantity
        buyer.trade_quantity = trade_quantity
        self.total_waste_traded += trade_quantity
        return

    def get_seller_from_list(self, index) -> Seller:
        return self.sellers[index][2]

    def get_buyer_from_list(self, index) -> Buyer:
        return self.buyers[index][2]

    def update_variables_seller(self, seller, daily_demand) -> None:
        seller.daily_demand = daily_demand
        self.total_waste_produced += seller.waste_left
        self.total_cost_without_trading_seller += \
            seller.waste_left * seller.cost_per_unit_waste_disposed

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
        buyer.daily_demand = daily_demand
        self.total_cost_without_trading_buyer += \
            buyer.input * buyer.cost_per_new_input

        if buyer.is_matched:
            cost = (buyer.input - buyer.trade_quantity) * \
                buyer.cost_per_new_input + \
                buyer.trade_quantity * buyer.trade_cost
            self.total_cost_with_trading_buyer += cost
        else:
            self.total_cost_with_trading_buyer += \
                buyer.input * buyer.cost_per_new_input
        return

    def plan_capacity(self, agent) -> None:
        if self.steps < 7:
            return
        if agent.capacity_planning_strategy is CapacityPlanningStrategies.lead:
            print('lead')
        elif agent.capacity_planning_strategy is CapacityPlanningStrategies.match:
            print('match')
        elif agent.capacity_planning_strategy is CapacityPlanningStrategies.lag:
            print('lag')
        else:
            raise Exception





















