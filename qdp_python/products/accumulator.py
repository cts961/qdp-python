from qdp_python import *


class Accumulator:
    def __init__(self,
                 initial_spot,
                 start_date,
                 maturity_date,
                 barrier,
                 strike,
                 call_multiplier,
                 put_multiplier
                 ):
        self.spot = initial_spot
        self.start_date = start_date
        self.maturity_date = maturity_date
        self.barrier = barrier
        self.strike = strike
        self.call_multiplier = call_multiplier
        self.put_multiplier = put_multiplier
        self.observation_dates = barrier.observation_dates

    def pv_by_path(self, dates, st, df):
        payoff_call = VanillaPayoff(PayoffType.Call, self.strike, self.call_multiplier)
        payoff_put = VanillaPayoff(PayoffType.Put, self.strike, self.put_multiplier)
        pv = 0
        for t in range(1, len(dates)):  # starts from 1 because this is the 1st settlement day
            d = dates[t]
            s = st[t]
            if self.barrier.is_hit(d, s):
                break
            pv += (payoff_call.pay(s, t) - payoff_put.pay(s, t)) * df[t]
        return pv

    def pv(self, engine):
        return engine.calc_pv(self)
