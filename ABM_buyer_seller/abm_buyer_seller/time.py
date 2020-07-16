from mesa.time import SimultaneousActivation
from mesa import Agent
from abm_buyer_seller.agents import WasteAgent
from abm_buyer_seller.agents import Buyer, Seller
import bisect


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

    def __init__(self, model) -> None:
        super().__init__(model)
        self.sellers = []
        self.buyers = []

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
        Finally, execues the advance of all agents.
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
        for i in range(len(self.sellers)):
        # for i in range(2):
            seller = self.get_seller_from_list(i)
            seller.step()
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

        for i in range(len(self.buyers)):
        # for i in range(2):
            buyer = self.get_buyer_from_list(i)
            buyer.step()
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

        for agent in self.agent_buffer(shuffled=False):
            agent.advance()

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
























    # def match_agents(self) -> None:
    #     # self.print_matched_state()
    #     self.initialise_agents()
    #     self.print_matched_state()
    #     print()
    #     i = 0
    #     j = 0
    #     while True:
    #         print(i, j)
    #         seller = self.get_seller_from_list(i)
    #         #print("current seller:", seller)
    #         buyer = self.get_buyer_from_list(i)
    #         #print("current buyer:", buyer)
    #         seller_has_waste_left = seller.waste_left > 0
    #         buyer_has_enough_capacity = buyer.capacity_left > 0
    #
    #         if not seller_has_waste_left:
    #             print('Seller has no more waste')
    #             print("current seller:", seller)
    #             print("current buyer:", buyer)
    #             if i == (self.seller_count - 1):
    #                 break
    #             i += 1
    #             continue
    #         if not buyer_has_enough_capacity:
    #             print('Buyer doesn\'t have enough capacity')
    #             print("current seller:", seller)
    #             print("current buyer:", buyer)
    #             if j == (self.buyer_count - 1):
    #                 break
    #             j += 1
    #             continue
    #         if seller.min_price <= buyer.max_price:
    #             self.prepare_trade(seller, buyer)
    #             print("current seller:", seller)
    #             print("current buyer:", buyer)
    #
    #             if i == (self.seller_count - 1) or j == (self.buyer_count - 1):
    #                 break
    #             i += 1
    #             j += 1
    #
    # def initialise_agents(self) -> None:  # seems super inefficient though
    #     """ Resets the is_matched variable of all agents to False"""
    #     for agent in self.agents:
    #         agent.trade_quantity = 0
    #
    # @property
    # def seller_count(self) -> int:
    #     return len(self.sellers)
    #
    # @property
    # def buyer_count(self) -> int:
    #     return len(self.buyers)
    #
    # @staticmethod
    # def prepare_trade(seller, buyer) -> None:
    #     seller.buyer = buyer
    #     buyer.seller = seller
    #     seller.is_matched = True
    #     buyer.is_matched = True
    #
    #     cost = (seller.min_price + buyer.max_price) / 2
    #     buyer.cost = cost
    #
    #     seller_quantity = seller.monthly_waste_produced
    #     buyer_quantity = buyer.monthly_capacity
    #     trade_quantity = min(seller_quantity, buyer_quantity)
    #     seller.trade_quantity = trade_quantity
    #     buyer.trade_quantity = trade_quantity
    #
    # # def get_agent_from_list(self, index, agent_type) -> Agent:
    # #     if agent_type == 'Seller':
    # #         return self.sellers[index][2]
    # #     assert agent_type == 'Buyer', 'type is neither Buyer not Seller'
    # #     return self.buyers[index][2]
    #
    # def get_seller_from_list(self, index) -> Seller:
    #     return self.sellers[index][2]
    #
    # def get_buyer_from_list(self, index) -> Buyer:
    #     return self.buyers[index][2]
    #
    # def print_matched_state(self) -> None:  # useless method to be deleted
    #     print('sellers matched state')
    #     for i in range(len(self.sellers)):
    #         seller = self.get_seller_from_list(i)
    #         print(seller.unique_id, seller.is_matched)
    #     print('buyers matched state')
    #     for i in range(len(self.buyers)):
    #         buyer = self.get_buyer_from_list(i)
    #         print(buyer.unique_id, buyer.is_matched)











