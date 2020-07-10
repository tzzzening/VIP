from mesa import Model
from abm_buyer_seller.time import SimultaneousActivationMoneyModel
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
        self.schedule = SimultaneousActivationMoneyModel(self)
        self.running = True
        # for i in range(num_per_agent):
            # seller = Seller(unique_id=self.next_id(), monthly_waste_produced=5,
            #                 min_price=5, model=self)
            # buyer = Buyer(unique_id=self.next_id(), monthly_capacity=3, max_price=5, model=self)
            # self.schedule.add(seller)
            # self.schedule.add(buyer)

        seller = Seller(unique_id=self.next_id(), monthly_waste_produced=5, min_price=6, model=self)
        self.schedule.add(seller)
        buyer = Buyer(unique_id=self.next_id(), monthly_capacity=25, max_price=7, model=self)
        self.schedule.add(buyer)
        seller = Seller(unique_id=self.next_id(), monthly_waste_produced=5, min_price=6, model=self)
        self.schedule.add(seller)
        buyer = Buyer(unique_id=self.next_id(), monthly_capacity=25, max_price=7, model=self)
        self.schedule.add(buyer)
        seller = Seller(unique_id=self.next_id(), monthly_waste_produced=5, min_price=6, model=self)
        self.schedule.add(seller)
        buyer = Buyer(unique_id=self.next_id(), monthly_capacity=25, max_price=7, model=self)
        self.schedule.add(buyer)
        seller = Seller(unique_id=self.next_id(), monthly_waste_produced=5, min_price=6, model=self)
        self.schedule.add(seller)
        buyer = Buyer(unique_id=self.next_id(), monthly_capacity=25, max_price=7, model=self)
        self.schedule.add(buyer)
        seller = Seller(unique_id=self.next_id(), monthly_waste_produced=5, min_price=6, model=self)
        self.schedule.add(seller)
        buyer = Buyer(unique_id=self.next_id(), monthly_capacity=25, max_price=7, model=self)
        self.schedule.add(buyer)

        self.match_agents()
        print('match with who')
        for i in self.schedule.sellers:
            print(i[2].unique_id, i[2].buyer)

    def step(self) -> None:
        self.num_steps += 1
        print('steps', self.num_steps)
        self.schedule.step()

    def __str__(self) -> str:
        return "\nCurrent Status:\n" + self.schedule.__str__()  # to print in order of price

    def match_agents(self) -> None:
        i = 0
        j = 0
        while True:
            print(i, j)
            seller = self.get_seller_from_list(i)
            # print(seller.unique_id)
            buyer = self.get_buyer_from_list(j)
            # print(buyer.unique_id)
            if seller.min_price > buyer.max_price:
                if j == (self.buyer_count - 1):
                    break
                j += 1
                continue

            self.prepare_trade(seller, buyer)
            if i == (self.seller_count - 1) or j == (self.buyer_count - 1):
                break
            i += 1
            j += 1
        return

    def get_seller_from_list(self, index) -> Seller:
        return self.schedule.sellers[index][2]

    def get_buyer_from_list(self, index) -> Buyer:
        return self.schedule.buyers[index][2]

    @property
    def seller_count(self) -> int:
        return len(self.schedule.sellers)

    @property
    def buyer_count(self) -> int:
        return len(self.schedule.buyers)

    @staticmethod
    def prepare_trade(seller, buyer) -> None:
        seller.buyer = buyer
        buyer.seller = seller
        seller.is_matched = True
        buyer.is_matched = True

        cost = (seller.min_price + buyer.max_price) / 2
        buyer.cost = cost
        return





