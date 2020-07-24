from mesa import Model
from abm_buyer_seller.time import SimultaneousActivationMoneyModel
from abm_buyer_seller.agents import Seller, Buyer
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


def compute_recycling_rate(model) -> float:
    print('MODEL')
    return model.total_waste_traded / model.total_waste_produced


def compute_seller_savings(model) -> float:
    money_saved = model.total_cost_without_trading_seller - model.total_cost_with_trading_seller
    return money_saved / model.total_cost_without_trading_seller


def compute_buyer_savings(model) -> float:
    money_saved = model.total_cost_without_trading_buyer - model.total_cost_with_trading_buyer
    return money_saved / model.total_cost_without_trading_buyer


def compute_overall_savings(model) -> float:
    total_costs_without_trading = \
        model.total_cost_without_trading_seller + model.total_cost_without_trading_buyer
    total_costs_with_trading = \
        model.total_cost_with_trading_seller + model.total_cost_with_trading_buyer
    money_saved = total_costs_without_trading - total_costs_with_trading
    return money_saved / total_costs_without_trading


class WasteModel(Model):
    """
    Testing 123.
    """

    # num_steps = 0
    total_waste_produced = 0
    total_waste_traded = 0
    # total_waste_traded_per_step = 0
    total_cost_without_trading_seller = 0  # cost incurred without trading waste, ie all waste is disposed of
    total_cost_with_trading_seller = 0
    total_cost_without_trading_buyer = 0  # cost incurred without trading waste, ie all waste is disposed of
    total_cost_with_trading_buyer = 0

    def __init__(self, seller_num, buyer_num, width, height) -> None:
        super().__init__()
        # print('MODEL INIT')
        self.seller_num = seller_num
        self.buyer_num = buyer_num
        self.width = width
        self.height = height
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = SimultaneousActivationMoneyModel(self)
        self.running = True
        self.steps = 0


        # for i in range(seller_num):
        #     seller = Seller(unique_id=self.next_id(), monthly_waste_produced=5,
        #                     min_price=5, model=self)
        #     self.schedule.add(seller)
        # for i in range(buyer_num):
        #     buyer = Buyer(unique_id=self.next_id(), monthly_capacity=4, max_price=5, model=self)
        #     self.schedule.add(buyer)

        seller = Seller(unique_id=self.next_id(), monthly_waste_produced=5, min_price=5, capacity=5, model=self)
        self.schedule.add(seller)
        buyer = Buyer(unique_id=self.next_id(), monthly_capacity=3, max_price=5, model=self)
        self.schedule.add(buyer)
        seller = Seller(unique_id=self.next_id(), monthly_waste_produced=5, min_price=5, capacity=5, model=self)
        self.schedule.add(seller)
        buyer = Buyer(unique_id=self.next_id(), monthly_capacity=25, max_price=5, model=self)
        self.schedule.add(buyer)

        self.match_agents()
        # print('match with who')
        # for i in self.schedule.sellers:
        #     print(i[2].unique_id, i[2].buyer)
        self.data_collector = DataCollector(
            model_reporters={'Recycling_Rate': compute_recycling_rate,
                             'Seller_Savings': compute_seller_savings,
                             'Buyer_Savings': compute_buyer_savings,
                             'Overall_Savings': compute_overall_savings},
            agent_reporters=None)

    def step(self) -> None:
        # print('before: produced {} traded {}'.format(self.total_waste_produced, self.total_waste_traded))
        # print('before seller costs savings: trade {} no {}'.
        #       format(self.total_cost_with_trading_seller, self.total_cost_without_trading_seller))
        # print('before buyer costs savings: trade {} no {}'.
        #       format(self.total_cost_with_trading_buyer, self.total_cost_without_trading_buyer))

        self.steps = self.schedule.steps
        print('step', self.steps)
        self.schedule.step()
        self.total_waste_produced = self.schedule.total_waste_produced
        self.total_waste_traded = self.schedule.total_waste_traded
        self.total_cost_without_trading_seller = self.schedule.total_cost_without_trading_seller
        self.total_cost_with_trading_seller = self.schedule.total_cost_with_trading_seller
        self.total_cost_without_trading_buyer = self.schedule.total_cost_without_trading_buyer
        self.total_cost_with_trading_buyer = self.schedule.total_cost_with_trading_buyer
        # print('after: produced {} traded {}'.format(self.total_waste_produced, self.total_waste_traded))
        # print('after seller costs savings: trade {} no {}'.
        #       format(self.total_cost_with_trading_seller, self.total_cost_without_trading_seller))
        # print('after buyer costs savings: trade {} no {}'.
        #       format(self.total_cost_with_trading_buyer, self.total_cost_without_trading_buyer))
        # print('seller saving', compute_seller_savings(self))
        # print('buyer saving', compute_buyer_savings(self))
        # print('overall saving', compute_overall_savings(self))
        self.data_collector.collect(self)

    def __str__(self) -> str:
        return "\nCurrent Status:\n" + self.schedule.__str__()  # to print in order of price

    def match_agents(self) -> None:
        """
        Match agents according to minimum price of the seller and the maximum price of the buyer.
        """
        i = 0
        j = 0
        while True:
            print(i, j)
            seller = self.get_seller_from_list(i)
            # print(seller.unique_id)
            buyer = self.get_buyer_from_list(j)
            # print(buyer.unique_id)
            if seller.min_price > buyer.max_price:
                if j == (self.buyer_num - 1):
                    break
                j += 1
                continue

            self.prepare_trade(seller, buyer)
            # if i == (self.seller_num - 1) or j == (self.buyer_num - 1):
            if i == 1 or j == 1:
                break
            i += 1
            j += 1
        return

    def get_seller_from_list(self, index) -> Seller:
        return self.schedule.sellers[index][2]

    def get_buyer_from_list(self, index) -> Buyer:
        return self.schedule.buyers[index][2]

    # @property
    # def seller_count(self) -> int:
    #     return len(self.schedule.sellers)
    #
    # @property
    # def buyer_count(self) -> int:
    #     return len(self.schedule.buyers)

    @staticmethod
    def prepare_trade(seller, buyer) -> None:
        """
        Update the trading partners and the cost per unit waste of each agent.
        :param seller:
        :param buyer:
        """

        seller.buyer = buyer
        buyer.seller = seller
        seller.is_matched = True
        buyer.is_matched = True

        cost = (seller.min_price + buyer.max_price) / 2
        seller.trade_cost = cost
        buyer.trade_cost = cost
        return





