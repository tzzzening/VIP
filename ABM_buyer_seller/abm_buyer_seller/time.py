from mesa.time import BaseScheduler
from mesa.agent import Agent
from abm_buyer_seller.agents import Buyer, Seller
import bisect


class BaseSchedulerMoneyModel(BaseScheduler):
    """
    BaseScheduler class with added lists to store buyers and sellers separately.
    """

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

    def match_agents(self) -> None:
        self.initialise_agents()

        i = 0
        j = 0
        while True:
            print(i, j)
            seller = self.get_agent_from_list(i, 'Seller')
            #print("current seller:", seller)
            buyer = self.get_agent_from_list(i, 'Buyer')
            #print("current buyer:", buyer)
            seller_has_goods_left = seller.goods_left > 0
            buyer_has_enough_capacity = buyer.monthly_capacity > 0

            if not seller_has_goods_left:
                print('Seller has no more waste')
                print("current seller:", seller)
                print("current buyer:", buyer)
                if i == (self.seller_count - 1):
                    break
                i += 1
                continue
            if not buyer_has_enough_capacity:
                print('Buyer doesn\'t have enough capacity')
                print("current seller:", seller)
                print("current buyer:", buyer)
                if j == (self.buyer_count - 1):
                    break
                j += 1
                continue
            if seller.min_price <= buyer.max_price:
                self.prepare_trade(seller, buyer)
                print("current seller:", seller)
                print("current buyer:", buyer)

                if i == (self.seller_count - 1) or j == (self.buyer_count - 1):
                    break
                i += 1
                j += 1

    def initialise_agents(self) -> None:  # seems super inefficient though
        """ Resets the is_matched variable of all agents to False"""
        for agent in self.agents:
            agent.is_matched = False

    @property
    def seller_count(self) -> int:
        return len(self.sellers)

    @property
    def buyer_count(self) -> int:
        return len(self.buyers)

    def print_lists(self) -> None:
        for i in self.sellers:
            print(i)
        for i in self.buyers:
            print(i)

    @staticmethod
    def prepare_trade(seller, buyer) -> None:
        seller.buyer = buyer
        buyer.seller = seller
        seller.is_matched = True
        buyer.is_matched = True

        cost = (seller.min_price + buyer.max_price) / 2
        buyer.cost = cost

        seller_quantity = seller.goods_left
        buyer_quantity = buyer.monthly_capacity
        trade_quantity = min(seller_quantity, buyer_quantity)
        seller.trade_quantity = trade_quantity
        buyer.trade_quantity = trade_quantity

    def get_agent_from_list(self, index, agent_type) -> Agent:
        if agent_type == 'Seller':
            return self.sellers[index][2]
        assert agent_type == 'Buyer', 'type is neither Buyer not Seller'
        return self.buyers[index][2]









