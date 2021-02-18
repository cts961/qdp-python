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
    def __init__(self, payoff_type: PayoffType, strike: float):
        super().__init__(lambda s: max((s - strike) * payoff_type, 0))


class CashOrNothingPayoff(Payoff):
    def __init__(self, payoff_type: PayoffType, strike: float, cash_amount: float):
        super().__init__(lambda s: np.sign(max((s - strike) * payoff_type, 0)) * cash_amount)


class AssetOrNothingPayoff(Payoff):
    def __init__(self, payoff_type: PayoffType, strike: float):
        super().__init__(lambda s: np.sign(max((s - strike) * payoff_type, 0)) * s)


class BarrierPayoff(Payoff):
    def __init__(self, payoff_type, barrier_type, barrier, strike):
        self.payoff_type = payoff_type
        self.barrier_type = barrier_type
        self.strike = strike
        self.barrier = barrier
        super().__init__(self.payoff_func)

    def barrier_factor(self, spot: float):
        if (self.barrier_type == BarrierType.UpOut and spot <= self.barrier
                or self.barrier_type == BarrierType.UpIn and spot > self.barrier
                or self.barrier_type == BarrierType.DownIn and spot < self.barrier
                or self.barrier_type == BarrierType.DownOut and spot >= self.barrier):
            return 1.0
        return 0

    def payoff_func(self, spot: float):
        return self.barrier_factor(spot) * VanillaPayoff(self.payoff_type, self.strike).pay(spot)
