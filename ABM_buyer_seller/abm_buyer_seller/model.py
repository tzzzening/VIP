from mesa import Model
from abm_buyer_seller.time import SimultaneousActivationMoneyModel
from abm_buyer_seller.agents import Seller, Buyer
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import random
import pandas as pd
import xlsxwriter


def compute_recycling_rate(model) -> float:
    # print('MODEL')
    return model.total_waste_traded / model.total_waste_produced


def compute_seller_savings(model) -> float:
    money_saved = model.total_profit_without_trading_seller - model.total_profit_with_trading_seller
    return money_saved / model.total_profit_without_trading_seller


def compute_buyer_savings(model) -> float:
    money_saved = model.total_profit_without_trading_buyer - model.total_profit_with_trading_buyer
    return money_saved / model.total_profit_without_trading_buyer


def compute_overall_savings(model) -> float:
    total_profit_without_trading = \
        model.total_profit_without_trading_seller + model.total_profit_without_trading_buyer
    total_profit_with_trading = \
        model.total_profit_with_trading_seller + model.total_profit_with_trading_buyer
    money_saved = total_profit_without_trading - total_profit_with_trading
    return money_saved / total_profit_without_trading


count = 0
data_dict = {'hello': ['bye']}

data = pd.DataFrame(data_dict)
data_to_excel = pd.ExcelWriter('ABM_data.xlsx', engine='xlsxwriter')
data.to_excel(data_to_excel, sheet_name='Sheet1')
data_to_excel.save()
count += 1
print(count)

class WasteModel(Model):
    """
    Testing 123.
    """

    total_waste_produced = 0
    total_waste_traded = 0
    total_profit_without_trading_seller = 0  # cost incurred without trading waste, ie all waste is disposed of
    total_profit_with_trading_seller = 0
    total_profit_without_trading_buyer = 0  # cost incurred without trading waste, ie all waste is disposed of
    total_profit_with_trading_buyer = 0

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


        for i in range(seller_num):
            seller = Seller(unique_id=self.next_id(),
                            min_price=random.randint(10, 14),
                            production_capacity=random.randint(160, 200),
                            model=self)
            self.schedule.add(seller)
        for i in range(buyer_num):
            buyer = Buyer(unique_id=self.next_id(),
                          waste_treatment_capacity=random.randint(40, 60),
                          max_price=random.randint(12, 16),
                          production_capacity=random.randint(150, 190),
                          model=self)
            self.schedule.add(buyer)

        # seller = Seller(unique_id=self.next_id(), min_price=12, production_capacity=180, model=self)
        # self.schedule.add(seller)
        # buyer = Buyer(unique_id=self.next_id(), waste_treatment_capacity=50, max_price=14,
        #               production_capacity=170, model=self)
        # self.schedule.add(buyer)

        # self.match_agents()
        self.data_collector = DataCollector(
            model_reporters={'Recycling_Rate': compute_recycling_rate,
                             'Seller_Savings': compute_seller_savings,
                             'Buyer_Savings': compute_buyer_savings,
                             'Overall_Savings': compute_overall_savings},
            agent_reporters=None)

    def step(self) -> None:
        # print('before: produced {} traded {}'.format(self.total_waste_produced, self.total_waste_traded))
        # print('before seller costs savings: trade {} no {}'.
        #       format(self.total_profit_with_trading_seller, self.total_profit_without_trading_seller))
        # print('before buyer costs savings: trade {} no {}'.
        #       format(self.total_profit_with_trading_buyer, self.total_profit_without_trading_buyer))

        self.steps = self.schedule.steps
        # print('step', self.steps)
        self.schedule.step()
        self.total_waste_produced = self.schedule.total_waste_produced
        self.total_waste_traded = self.schedule.total_waste_traded
        self.total_profit_without_trading_seller = self.schedule.total_profit_without_trading_seller
        self.total_profit_with_trading_seller = self.schedule.total_profit_with_trading_seller
        self.total_profit_without_trading_buyer = self.schedule.total_profit_without_trading_buyer
        self.total_profit_with_trading_buyer = self.schedule.total_profit_with_trading_buyer
        # print('after: produced {} traded {}'.format(self.total_waste_produced, self.total_waste_traded))
        # print('after seller costs savings: trade {} no {}'.
        #       format(self.total_profit_with_trading_seller, self.total_profit_without_trading_seller))
        # print('after buyer costs savings: trade {} no {}'.
        #       format(self.total_profit_with_trading_buyer, self.total_profit_without_trading_buyer))
        if self.steps == 2:
            print('recycling rate', compute_recycling_rate(self))
            print('seller saving', compute_seller_savings(self))
            print('buyer saving', compute_buyer_savings(self))
            print('overall saving', compute_overall_savings(self))
            print()
            recycling_rate = compute_recycling_rate(self)
            seller_savings = compute_seller_savings(self)
            buyer_savings = compute_buyer_savings(self)
            overall_savings = compute_overall_savings(self)
            data_dict[str(count)] = [str(recycling_rate), str(seller_savings), str(buyer_savings), str(overall_savings)]
            # data = pd.DataFrame({'data': [recycling_rate,
            #                               seller_savings,
            #                               buyer_savings,
            #                               overall_savings]})
            # # data = pd.DataFrame({'data': [1, 2, 3]})
            # data_to_excel = pd.ExcelWriter('ABM_data.xlsx', engine='xlsxwriter')
            # data.to_excel(data_to_excel, sheet_name='Sheet1')
            # data_to_excel.save()
        self.data_collector.collect(self)

    def __str__(self) -> str:
        return "\nCurrent Status:\n" + self.schedule.__str__()  # to print in order of price






