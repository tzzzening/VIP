from mesa import Model
from abm_buyer_seller.time import BaseSchedulerMoneyModel
from abm_buyer_seller.agents import Seller, Buyer


class MoneyModel(Model):
    def __init__(self, num_per_agent) -> None:
        super().__init__()
        self.num_per_agent = num_per_agent
        self.schedule = BaseSchedulerMoneyModel(self)
        # for i in range(num_per_agent):
        #     seller = Seller(unique_id=self.next_id(), goods_left=5, min_price=5, model=self)
        #     buyer = Buyer(unique_id=self.next_id(), money_left=50, max_price=10, model=self)
        #     self.schedule.add(seller)
        #     self.schedule.add(buyer)

        seller = Seller(unique_id=self.next_id(), goods_left=6, min_price=2.5, model=self)
        self.schedule.add(seller)
        buyer = Buyer(unique_id=self.next_id(), money_left=24, max_price=7.5, model=self)
        self.schedule.add(buyer)
        # seller = Seller(unique_id=self.next_id(), goods_left=0, min_price=4, model=self)
        # self.schedule.add(seller)
        # buyer = Buyer(unique_id=self.next_id(), money_left=50, max_price=9, model=self)
        # self.schedule.add(buyer)

    def step(self) -> None:
        self.schedule.step()

    def __str__(self) -> str:
        # output = "\nCurrent status:\n"

        # to print in order of id
        # for i in self.schedule.agents:
        #     output += i.__str__()
        #     output += "\n"
        # return output

        return "\nCurrent Status:\n" + self.schedule.__str__()  # to print in order of price





