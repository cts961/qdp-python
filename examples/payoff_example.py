import matplotlib.pyplot as plt

from modules.payoff import *

# synthetic payoff construction
p1 = VanillaPayoff(PayoffType.Call, 1)
p2 = VanillaPayoff(PayoffType.Call, 1.15)

p3 = BarrierPayoff(PayoffType.Put, BarrierType.DownOut, 0.9, 1.0)

p4 = VanillaPayoff(PayoffType.Put, 0.9)

p = p1 - p2 + p3 - p4

s = np.linspace(0.5, 1.5, 1000)
payoff = []

for x in s:
    payoff.append(p.pay(x))

plt.plot(s, payoff)
plt.show()
