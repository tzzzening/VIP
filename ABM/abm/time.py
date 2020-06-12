from mesa.time import BaseScheduler
from mesa.agent import Agent
from abm.agents import Buyer, Seller
import bisect


class BaseSchedulerMoneyModel(BaseScheduler):
    """
    BaseScheduler class with added lists to store buyers and sellers separately.
    """

    def __init__(self, model):
        super().__init__(model)
        self.sellers = []
        self.buyers = []

    def __str__(self):
        output = ""
        for i in self.sellers:
            output += (i[2].__str__() + "\n")
        for i in self.buyers:
            output += (i[2].__str__() + "\n")
        return output

    def add(self, agent: Agent) -> None:
        self._agents[agent.unique_id] = agent
        if isinstance(agent, Seller):
            bisect.insort(self.sellers, (agent.min_price, agent.unique_id, agent))
        elif isinstance(agent, Buyer):
            bisect.insort(self.buyers, (agent.max_price, agent.unique_id, agent))
        else:
            raise Exception  # specify exception later, not sure about python exceptions

    def step(self) -> None:
        self.match_agents()
        for agent in self.agent_buffer(shuffled=False):
            agent.step()
        self.steps += 1
        self.time += 1

    def match_agents(self):
        self.initialise_agents()

        i = 0
        j = 0
        while True:  # remember to exit loop
            # print(i, j)
            seller = self.sellers[i][2]
            buyer = self.buyers[j][2]
            seller_has_goods_left = seller.goods_left > 0
            buyer_has_enough_money = buyer.money_left >= buyer.max_price

            if not seller_has_goods_left:
                if i == (self.get_per_agent_count() - 1):
                    break
                i += 1
                continue
            if not buyer_has_enough_money:
                if j == (self.get_per_agent_count() - 1):
                    break
                j += 1
                continue
            if seller.min_price <= buyer.max_price:
                seller.buyer = buyer
                buyer.seller = seller
                seller.is_matched = True
                buyer.is_matched = True
                if i == (self.get_per_agent_count() - 1) or j == (self.get_per_agent_count() - 1):
                    break
                i += 1
                j += 1

            # if seller_has_goods_left and buyer_has_enough_money:
            #     if seller.min_price <= buyer.max_price:
            #         seller.buyer = buyer
            #         buyer.seller = seller
            #         seller.is_matched = True
            #         buyer.is_matched = True
            #         # del self.sellers[0]
            #         # del self.buyers[0]

    def initialise_agents(self):  # seems super inefficient though
        """ Resets the is_matched variable of all agents to False"""
        for agent in self.agents:
            agent.is_matched = False

    def get_per_agent_count(self):
        return self.get_agent_count() // 2

    def print_lists(self):
        for i in self.sellers:
            print(i)
        for i in self.buyers:
            print(i)





