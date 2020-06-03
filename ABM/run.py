from abm.agents import Seller, Buyer
from abm.model import MoneyModel

# model = MoneyModel(1)
# seller = Seller(1, 5, 5, model)
# buyer = Buyer(1, 50, 10, model)
#
# while seller.num_of_goods > 0 and buyer.money >= seller.min_price:
#     if seller.min_price <= buyer.max_price:
#         seller.sell()
#         buyer.buy((seller.min_price + buyer.max_price) / 2)
#
# print(seller)
# print(buyer)

model = MoneyModel(1)
print(model)
model.step()
print(model)
