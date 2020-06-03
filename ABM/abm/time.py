from mesa.time import SimultaneousActivation
from mesa.agent import Agent
from abm.agents import Buyer, Seller
from abm.priority_queue import SellerPriorityQueue, BuyerPriorityQueue


class SimultaneousActivationMoneyModel(SimultaneousActivation):
    """
    SimultaneousActivation class with added priority queues to store buyers and sellers separately.
    """

    def __init__(self, model):
        super().__init__(model)
        self.sellers = SellerPriorityQueue()
        self.buyers = BuyerPriorityQueue()

    def add(self, agent: Agent) -> None:
        self._agents[agent.unique_id] = agent
        if isinstance(agent, Seller):
            self.sellers.put_in_queue(agent)
        elif isinstance(agent, Buyer):
            self.buyers.put_in_queue(agent)
        else:
            raise Exception  # specify exception later, not sure about python exceptions

    def step(self) -> None:
        """ Step all agents, then advance them. """
        self.match_agents()
        # invoke step and advance methods of individual agents
        agent_keys = list(self._agents.keys())
        for agent_key in agent_keys:
            self._agents[agent_key].step()
        for agent_key in agent_keys:
            self._agents[agent_key].advance()
        self.steps += 1
        self.time += 1

    def match_agents(self):
        self.unmatch_agents()  # initialize is_matched status of all agents
        seller = self.sellers.queue[0][2]
        buyer = self.buyers.queue[0][2]
        seller_has_goods_left = seller.goods_left > 0
        buyer_has_enough_money = buyer.money_left >= seller.min_price

        if seller_has_goods_left and buyer_has_enough_money:
            if seller.min_price <= buyer.max_price:
                seller.buyer = buyer
                buyer.seller = seller
                seller.is_matched = True
                buyer.is_matched = True
                #self.sellers.pop_task()  # can consider changing to the remove_task stuff from pq
                #self.buyers.pop_task()

    def unmatch_agents(self):  # seems super inefficient though
        for agent in self.agents:
            agent.is_matched = False







