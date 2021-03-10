import numpy as np
from qdp_python.modules import BarrierType, BinaryType
from qdp_python.products import OptionType
from scipy.stats import norm


class AnalyticalBinaryOptionEngine:

    def __init__(self, process):
        self.process = process
        self.b = self.process.r - self.process.q
        self.v2 = self.process.v * self.process.v

    def calc_analytical_binary_european_option(self, option):
        engine = AnalyticalBinaryOptionEngine(self.process)

        if option.barrier.barrier_type == BinaryType.CashOrNothing:
            return engine.calc_cash_or_nothing(option)
        elif option.barrier.barrier_type == BinaryType.AssetOrNothing:
            return engine.calc_asset_or_nothing(option)
        else:
            raise TypeError("Binary Type Error")

    def calc_cash_or_nothing(self, option):
        T = self.process.day_counter.year_fraction(option.start_date, option.maturity_date)
        d = (np.log(option.spot / option.strike) + (self.b - self.v2 / 2)*T) / self.process.v / np.sqrt(T)

        if option.option_type == OptionType.Call:
            return option.rebate * np.exp(-self.process.r * T) * norm.cdf(d)
        else:
            return option.rebate * np.exp(-self.process.r * T) * norm.cdf(-d)

    def calc_asset_or_nothing(self, option):
        T = self.process.day_counter.year_fraction(option.start_date, option.maturity_date)
        d = (np.log(option.spot / option.strike) + (self.b + self.v2 / 2) * T) / self.process.v / np.sqrt(T)

        if option.option_type == OptionType.Call:
            return option.spot * np.exp((self.b-self.process.r) * T) * norm.cdf(d)
        else:
            return option.spot * np.exp((self.b-self.process.r) * T) * norm.cdf(-d)