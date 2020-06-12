from abm_buyer_seller.model import MoneyModel
import multiprocessing as mp
import numpy as np
from time import time


model = MoneyModel(10)
# model.schedule.print_lists()
print(model)
model.step()
print(model)

# np.random.RandomState(100)
# arr = np.random.randint(0, 10, size=[200000, 5])
# data = arr.tolist()
# data[:5]




