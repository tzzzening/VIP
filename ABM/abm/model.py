from mesa import Model
from abm.time import BaseSchedulerMoneyModel
from abm.agents import Seller, Buyer


class MoneyModel(Model):
    def __init__(self, num_per_agent):
        super().__init__()
        self.num_per_agent = num_per_agent
        self.schedule = BaseSchedulerMoneyModel(self)
        # for i in range(num_per_agent):
        #     seller = Seller(unique_id=self.next_id(), goods_left=5, min_price=5, model=self)
        #     buyer = Buyer(unique_id=self.next_id(), money_left=50, max_price=10, model=self)
        #     self.schedule.add(seller)
        #     self.schedule.add(buyer)
        seller = Seller(unique_id=self.next_id(), goods_left=5, min_price=5, model=self)
        buyer = Buyer(unique_id=self.next_id(), money_left=5, max_price=5, model=self)
        self.schedule.add(seller)
        self.schedule.add(buyer)
        seller = Seller(unique_id=self.next_id(), goods_left=5, min_price=5, model=self)
        buyer = Buyer(unique_id=self.next_id(), money_left=50, max_price=6, model=self)
        self.schedule.add(seller)
        self.schedule.add(buyer)

    def step(self):
        self.schedule.step()

    def __str__(self):
        output = "\nCurrent status:\n"
        for i in self.schedule.agents:
            output += i.__str__()
            output += "\n"
        return output



