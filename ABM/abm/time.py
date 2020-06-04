from mesa.time import BaseScheduler
from mesa.agent import Agent
from abm.agents import Buyer, Seller
from abm.priority_queue import SellerPriorityQueue, BuyerPriorityQueue
import bisect


class BaseSchedulerMoneyModel(BaseScheduler):
    """
    SimultaneousActivation class with added priority queues to store buyers and sellers separately.
    """

    def __init__(self, model):
        super().__init__(model)
        self.sellers = []
        self.buyers = []

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
        
        seller = self.sellers[0][2]
        buyer = self.buyers[0][2]
        seller_has_goods_left = seller.goods_left > 0
        buyer_has_enough_money = buyer.money_left >= buyer.max_price

        if seller_has_goods_left and buyer_has_enough_money:
            if seller.min_price <= buyer.max_price:
                seller.buyer = buyer
                buyer.seller = seller
                seller.is_matched = True
                buyer.is_matched = True
                del self.sellers[0]
                del self.buyers[0]

    def initialise_agents(self):  # seems super inefficient though
        """ Resets the is_matched variable of all agents to False"""
        for agent in self.agents:
            agent.is_matched = False







