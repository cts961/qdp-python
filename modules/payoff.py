import numpy as np
from modules.barrier import *


class PayoffType(enumerate):
    Call = 1.0
    Put = -1.0


class Payoff:
    def __init__(self, payoff_func):
        self.payoff_func = payoff_func

    def pay(self, spot: float) -> float:
        return self.payoff_func(spot)

    def __neg__(self):
        return Payoff(lambda s: -self.payoff_func(s))

    def __add__(self, other):
        return Payoff(lambda s: self.payoff_func(s) + other.payoff_func(s))

    def __sub__(self, other):
        return Payoff(lambda s: self.payoff_func(s) - other.payoff_func(s))


class VanillaPayoff(Payoff):
    def __init__(self, payoff_type: PayoffType, strike=None, participation_rate=1.0):
        self._strike = strike
        self._payoff_type = payoff_type
        self._participation_rate = participation_rate
        super().__init__(self.pay)

    @property
    def strike(self):
        return self._strike

    @strike.setter
    def strike(self, strike):
        self._strike = strike

    def pay(self, spot: float):
        return max((spot - self._strike) * self._payoff_type, 0) * self._participation_rate


class CashOrNothingPayoff(Payoff):
    def __init__(self, payoff_type: PayoffType, strike=None, cash_amount=None):
        self._payoff_type = payoff_type
        self._strike = strike
        self._cash_amount = cash_amount
        super().__init__(self.pay)

    @property
    def strike(self):
        return self._strike

    @strike.setter
    def strike(self, strike):
        self._strike = strike

    @property
    def cash(self):
        return self._cash_amount

    @cash.setter
    def cash(self, cash_amount):
        self._cash_amount = cash_amount

    def pay(self, spot):
        return np.sign(max((spot - self._strike) * self._payoff_type, 0)) * self._cash_amount


class AssetOrNothingPayoff(Payoff):
    def __init__(self, payoff_type: PayoffType, strike: float):
        super().__init__(lambda s: np.sign(max((s - strike) * payoff_type, 0)) * s)


class BarrierPayoff(Payoff):
    def __init__(self, payoff_type, barrier_type, barrier, strike, participation_rate=1.0):
        self.payoff_type = payoff_type
        self.barrier_type = barrier_type
        self.strike = strike
        self.barrier = barrier
        self._participation_rate = participation_rate
        super().__init__(self.payoff_func)

    def barrier_factor(self, spot: float):
        if (self.barrier_type == BarrierType.UpOut and spot <= self.barrier
                or self.barrier_type == BarrierType.UpIn and spot > self.barrier
                or self.barrier_type == BarrierType.DownIn and spot < self.barrier
                or self.barrier_type == BarrierType.DownOut and spot >= self.barrier):
            return 1.0
        return 0

    def payoff_func(self, spot: float):
        bf = self.barrier_factor(spot)
        vp = VanillaPayoff(self.payoff_type, self.strike, self._participation_rate)
        return bf * vp.pay(spot)
