from abm_buyer_seller.model import WasteModel
import multiprocessing as mp
import numpy as np
from time import time
import matplotlib.pyplot as plt
from mesa.batchrunner import BatchRunner

# from abm_buyer_seller.server import server
# server.launch()








def compute_recycling_rate(model) -> float:
    # print('RUN')
    return model.total_waste_traded / model.total_waste_produced


def compute_seller_savings(model) -> float:
    money_saved = model.total_profit_without_trading_seller - model.total_profit_with_trading_seller
    return money_saved / model.total_profit_without_trading_seller


def compute_buyer_savings(model) -> float:
    money_saved = model.total_profit_without_trading_buyer - model.total_profit_with_trading_buyer
    return money_saved / model.total_profit_without_trading_buyer


def compute_overall_savings(model) -> float:
    total_costs_without_trading = \
        model.total_profit_without_trading_seller + model.total_profit_without_trading_buyer
    total_costs_with_trading = \
        model.total_profit_with_trading_seller + model.total_profit_with_trading_buyer
    money_saved = total_costs_without_trading - total_costs_with_trading
    return money_saved / total_costs_without_trading


fixed_params = {'width': 1, 'height': 1}
variable_params = {'seller_num': range(2, 3), 'buyer_num': range(2, 3)}
# fixed_params = {'width': 1, 'height': 1, 'num_per_agent': 2}
# variable_params = None
batch_run = BatchRunner(WasteModel, variable_params, fixed_params,
                        iterations=1, max_steps=300,
                        model_reporters={'Recycling_Rate': compute_recycling_rate,
                                         'Seller_Savings': compute_seller_savings,
                                         'Buyer_Savings': compute_buyer_savings,
                                         'Overall_Savings': compute_overall_savings
                                         })
batch_run.run_all()
run_data = batch_run.get_model_vars_dataframe()
run_data.head()
plot_list = [1]
plt.scatter(plot_list, run_data.Recycling_Rate)
plt.scatter(plot_list, run_data.Seller_Savings)
plt.scatter(plot_list, run_data.Buyer_Savings)
plt.scatter(plot_list, run_data.Overall_Savings)
# plt.show()



