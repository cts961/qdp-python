import matplotlib.pyplot as plt

from modules.payoff import *

# synthetic payoff construction

p1 = VanillaPayoff(PayoffType.Call, 1)
p2 = VanillaPayoff(PayoffType.Call, 1.15)

p3 = BarrierPayoff(PayoffType.Put, BarrierType.DownOut, 0.9, 1.0)

p4 = VanillaPayoff(PayoffType.Put, 0.9)


class Coupon:
    def __init__(self, d0, r):
        self.d0 = d0
        self.r = r

    def __getitem__(self, d1):
        return (d1 - self.d0) * self.r


cash = Coupon(0, 0.2)
# p5 has a subscriptable arguments, make p5 pay function has an extra dependent variable t
p5 = CashOrNothingPayoff(PayoffType.Call, 1.0, cash)

# p contains p5
# so p pay function has the form of pay(s, t)
p = p1 - p2 + p3 - p4 + p5

s = np.linspace(0.5, 1.5, 1000)
payoff = []

for x in s:
    payoff.append(p.pay(x, 1))

plt.plot(s, payoff)
plt.show()
