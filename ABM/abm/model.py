from mesa import Model
from mesa.time import BaseScheduler
from abm.agents import WasteGenerator, WasteReceiver


class WasteModel(Model):
    def __init__(self, num_generators, num_receivers):
        super().__init__()
        self.num_generators = num_generators
        self.num_receivers = num_receivers
        self.schedule = BaseScheduler(self)

        for i in range(num_generators):
            generator = WasteGenerator(self.next_id(), 1, self)
            self.schedule.add(generator)

        for i in range(num_receivers):
            receiver = WasteReceiver(self.next_id(), self)
            self.schedule.add(receiver)

    def step(self) -> None:
        self.schedule.step()









