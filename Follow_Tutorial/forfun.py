# from statistics import mean
# import numpy as np
#
# xs = np.array([1, 2, 3, 4, 5], dtype=np.float64)
# ys = np.array([2, 4, 6, 8, 10], dtype=np.float64)
#
#
# def best_fit_slope_and_intercept(xs, ys):
#     m = (((mean(xs) * mean(ys)) - mean(xs * ys)) /
#          ((mean(xs) * mean(xs)) - mean(xs * xs)))
#
#     b = mean(ys) - m * mean(xs)
#
#     return m, b
#
#
# m, b = best_fit_slope_and_intercept(xs, ys)
#
# print(m, b)



import random
random.seed(1)
for i in range(28):
    print(random.randint(5, 10))