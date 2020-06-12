from mesa import Agent


class WasteGenerator(Agent):
    def __init__(self, unique_id, waste_generated, model) -> None:
        super().__init__(unique_id, model)
        self.waste_generated = waste_generated

    def step(self) -> None:
        self.give_waste()

    def give_waste(self) -> None:
        print('waste given')


class WasteReceiver(Agent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)
        self.waste_received = 0

    def step(self) -> None:
        self.collect_waste()

    def collect_waste(self) -> None:
        print("waste received")
        self.waste_received += 1








