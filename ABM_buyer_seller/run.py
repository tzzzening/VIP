from abm_buyer_seller.model import MoneyModel
import multiprocessing as mp
import numpy as np
from time import time
import matplotlib.pyplot as plt


model = MoneyModel(10)
# model.schedule.print_lists()
print(model)
model.step()
print(model)

# np.random.RandomState(100)
# arr = np.random.randint(0, 10, size=[200000, 5])
# data = arr.tolist()
# data[:5]

# seller_goods = [s[2].goods_left for s in model.schedule.sellers]
# plt.hist(seller_goods)
buyer_money = [b[2].money_left for b in model.schedule.buyers]
plt.hist(buyer_money)
plt.show()



