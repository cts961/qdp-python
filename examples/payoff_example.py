from qdp_python import *

p1 = VanillaPayoff(PayoffType.Call, 1)
p2 = VanillaPayoff(PayoffType.Call, 1.15)

p3 = BarrierPayoff(PayoffType.Put, BarrierType.DownOut, 0.9, 1.0)

p4 = VanillaPayoff(PayoffType.Put, 0.9)


# p = p1 - p2 + p3 - p4
#
# import matplotlib.pyplot as plt
# import numpy as np
#
# xs = np.linspace(0.5, 1.5, 1000)
# payoff = []
# for x in xs:
#     payoff.append(p.pay(x))
#
# plt.plot(xs, payoff)
# plt.show()

coupon_rate = InterestRate(0.2)
ko_coupon = Coupon(Date(2021, 2, 23), 100, coupon_rate)

p = CashOrNothingPayoff(PayoffType.Call, 100, ko_coupon)

print(p.pay(101, Date(2021, 8, 23)))