from mesa import Model
from abm_buyer_seller.time import BaseSchedulerMoneyModel
from abm_buyer_seller.agents import Seller, Buyer
import random


class MoneyModel(Model):
    def __init__(self, num_per_agent) -> None:
        super().__init__()
        self.num_per_agent = num_per_agent
        self.schedule = BaseSchedulerMoneyModel(self)
        for i in range(num_per_agent):
            seller = Seller(unique_id=self.next_id(), goods_left=random.randint(0, 11),
                            min_price=random.randint(5, 11), model=self)
            buyer = Buyer(unique_id=self.next_id(), money_left=random.randint(0, 11),
                          max_price=random.randint(7, 13), model=self)
            self.schedule.add(seller)
            self.schedule.add(buyer)



    def step(self) -> None:
        self.schedule.step()

    def __str__(self) -> str:
        return self.schedule.__str__()  # to print in order of price



