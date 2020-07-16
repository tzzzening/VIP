from abm_buyer_seller.model import WasteModel
import multiprocessing as mp
import numpy as np
from time import time
import matplotlib.pyplot as plt
from mesa.batchrunner import BatchRunner

# from abm_buyer_seller.server import server
# server.launch()

# model = WasteModel(10, 1, 1)
# # model.schedule.print_lists()
# print(model)
# model.step()
# print(model)

# np.random.RandomState(100)
# arr = np.random.randint(0, 10, size=[200000, 5])
# data = arr.tolist()
# data[:5]

# seller_goods = [s[2].goods_left for s in model.schedule.sellers]
# plt.hist(seller_goods)
# buyer_money = [b[2].money_left for b in model.schedule.buyers]






def compute_recycling_rate(model) -> float:
    print('RUN')
    return model.total_waste_traded / model.total_waste_produced


def compute_costs_savings_seller(model) -> float:
    money_saved = model.total_cost_without_trading_seller - model.total_cost_with_trading_seller
    return money_saved / model.total_cost_without_trading_seller


def compute_costs_savings_buyer(model) -> float:
    money_saved = model.total_cost_without_trading_buyer - model.total_cost_with_trading_buyer
    return money_saved / model.total_cost_without_trading_buyer


def compute_costs_savings(model) -> float:
    total_costs_without_trading = \
        model.total_cost_without_trading_seller + model.total_cost_without_trading_buyer
    total_costs_with_trading = \
        model.total_cost_with_trading_seller + model.total_cost_with_trading_buyer
    money_saved = total_costs_without_trading - total_costs_with_trading
    return money_saved / total_costs_without_trading


fixed_params = {'width': 1, 'height': 1}
variable_params = {'seller_num': range(1, 2), 'buyer_num': range(1, 2)}
# fixed_params = {'width': 1, 'height': 1, 'num_per_agent': 2}
# variable_params = None
batch_run = BatchRunner(WasteModel, variable_params, fixed_params,
                        iterations=2, max_steps=2,
                        model_reporters={'Recycling_Rate': compute_recycling_rate,
                                         'Costs_Savings_Seller': compute_costs_savings_seller,
                                         'Costs_Savings_Buyer': compute_costs_savings_buyer,
                                         'Costs_Savings_Overall': compute_costs_savings
                                         })
batch_run.run_all()
run_data = batch_run.get_model_vars_dataframe()
run_data.head()
plot_list = [1, 2]
plt.scatter(plot_list, run_data.Recycling_Rate)
plt.scatter(plot_list, run_data.Costs_Savings_Seller)
plt.scatter(plot_list, run_data.Costs_Savings_Buyer)
plt.scatter(plot_list, run_data.Costs_Savings_Overall)
plt.show()














# plt.hist(buyer_money)
# plt.show()



