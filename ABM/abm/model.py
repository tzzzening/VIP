from mesa import Model
from mesa.time import SimultaneousActivation
from abm.agents import Seller, Buyer


class MoneyModel(Model):
    def __init__(self, num_agents):
        self.num_agents = num_agents
        self.schedule = SimultaneousActivation(self)
        for i in range(num_agents):
            seller = Seller(i, 5, 5, self)
            buyer = Buyer(i, 50, 10, self)
            self.schedule.add(seller)
            self.schedule.add(buyer)

    def step(self):
        self.schedule.step()

    def __str__(self):
        output = "Current status:\n"
        for i in self.schedule.agents:
            output += i.__str__()
            output += "\n"
        return output



