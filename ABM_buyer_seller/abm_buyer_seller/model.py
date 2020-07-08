from mesa import Model
from abm_buyer_seller.time import BaseSchedulerMoneyModel
from abm_buyer_seller.agents import Seller, Buyer
from mesa.space import MultiGrid


class WasteModel(Model):

    num_steps = 0

    def __init__(self, num_per_agent, width, height) -> None:
        super().__init__()
        self.num_per_agent = num_per_agent
        self.width = width
        self.height = height
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = BaseSchedulerMoneyModel(self)
        self.running = True
        for i in range(num_per_agent):
            seller = Seller(unique_id=self.next_id(), monthly_waste_produced=5,
                            min_price=5, model=self)
            buyer = Buyer(unique_id=self.next_id(), monthly_capacity=4, max_price=5, model=self)
            self.schedule.add(seller)
            self.schedule.add(buyer)

        # seller = Seller(unique_id=self.next_id(), goods_left=5, min_price=5, model=self)
        # self.schedule.add(seller)
        # buyer = Buyer(unique_id=self.next_id(), money_left=25, max_price=5, capacity=4, model=self)
        # self.schedule.add(buyer)
        # seller = Seller(unique_id=self.next_id(), goods_left=5, min_price=5, model=self)
        # self.schedule.add(seller)
        # buyer = Buyer(unique_id=self.next_id(), money_left=25, max_price=5, capacity=4, model=self)
        # self.schedule.add(buyer)


    def step(self) -> None:
        self.num_steps += 1
        print('steps', self.num_steps)
        self.schedule.step()


    def __str__(self) -> str:
        # output = "\nCurrent status:\n"

        # to print in order of id
        # for i in self.schedule.agents:
        #     output += i.__str__()
        #     output += "\n"
        # return output

        return "\nCurrent Status:\n" + self.schedule.__str__()  # to print in order of price





