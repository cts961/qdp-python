import numpy as np
from modules.barrier import *


class PayoffType(enumerate):
    Call = 1.0
    Put = -1.0


def getvalue(k, t):
    if hasattr(k, "__getitem__"):
        if t is not None:
            return k[t]
        else:
            raise IndexError

    return k


class Payoff:
    def __init__(self, payoff_func):
        self.payoff_func = payoff_func

    def pay(self, spot: float, t=None) -> float:
        return self.payoff_func(spot, t)

    def __neg__(self):
        return Payoff(lambda s, t: -self.payoff_func(s, t))

    def __add__(self, other):
        return Payoff(lambda s, t: self.payoff_func(s, t) + other.payoff_func(s, t))

    def __sub__(self, other):
        return Payoff(lambda s, t: self.payoff_func(s, t) - other.payoff_func(s, t))


class VanillaPayoff(Payoff):
    def __init__(self, payoff_type: PayoffType, strike=None, participation_rate=1.0):
        self._strike = strike
        self._payoff_type = payoff_type
        self._participation_rate = participation_rate
        super().__init__(self.pay)

    def pay(self, spot: float, t=None):
        k = getvalue(self._strike, t)
        pr = getvalue(self._participation_rate, t)
        return max((spot - k) * self._payoff_type, 0) * pr


class CashOrNothingPayoff(Payoff):
    def __init__(self, payoff_type: PayoffType, strike=None, cash_amount=None):
        self._payoff_type = payoff_type
        self._strike = strike
        self._cash_amount = cash_amount
        super().__init__(self.pay)

    def pay(self, spot, t=None):
        k = getvalue(self._strike, t)
        c = getvalue(self._cash_amount, t)
        return np.sign(max((spot - k) * self._payoff_type, 0)) * c


class AssetOrNothingPayoff(Payoff):
    def __init__(self, payoff_type: PayoffType, strike):
        self._strike = strike
        self._payoff_type = payoff_type
        super().__init__(self.pay)

    def pay(self, spot, t=None):
        k = getvalue(self._strike, t)
        return np.sign(max((spot - k) * self._payoff_type, 0)) * spot


class BarrierPayoff(Payoff):
    def __init__(self, payoff_type, barrier_type, barrier, strike, participation_rate=1.0):
        self.payoff_type = payoff_type
        self.barrier_type = barrier_type
        self.strike = strike
        self.barrier = barrier
        self._participation_rate = participation_rate
        super().__init__(self.pay)

    def barrier_factor(self, spot: float, t=None):
        b = getvalue(self.barrier, t)

        if (self.barrier_type == BarrierType.UpOut and spot <= b
                or self.barrier_type == BarrierType.UpIn and spot > b
                or self.barrier_type == BarrierType.DownIn and spot < b
                or self.barrier_type == BarrierType.DownOut and spot >= b):
            return 1.0
        return 0

    def pay(self, spot: float, t=None):
        bf = self.barrier_factor(spot, t)
        vp = VanillaPayoff(self.payoff_type, self.strike, self._participation_rate)
        return bf * vp.pay(spot, t)
