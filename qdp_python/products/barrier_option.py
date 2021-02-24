from qdp_python import *


class BarrierOption:
    def __init__(self,
                 initial_spot,
                 start_date,
                 maturity_date,
                 barrier,
                 hit_payoff,
                 unhit_payoff):
        self.spot = initial_spot
        self.start_date = start_date
        self.maturity_date = maturity_date
        self.barrier = barrier
        self.hit_payoff = hit_payoff
        self.unhit_payoff = unhit_payoff

        self.observation_dates = sorted({maturity_date}.union(barrier.observation_dates))

    def pv_by_path(self, dates, st, df):
        if (self.barrier.barrier_type == BarrierType.UpOut) or (self.barrier.barrier_type == BarrierType.DownOut):
            for t in range(len(dates)):
                d = dates[t]
                s = st[t]
                if self.barrier.is_hit(d, s):
                    return self.hit_payoff.pay(s, d) * df[t]

            return self.unhit_payoff.pay(st[-1], dates[-1]) * df[-1]

        elif (self.barrier.barrier_type == BarrierType.UpIn) or (self.barrier.barrier_type == BarrierType.DownIn):
            for t in range(len(dates)):
                d = dates[t]
                s = st[t]
                if self.barrier.is_hit(d, s):
                    return self.hit_payoff.pay(st[-1], dates[-1]) * df[-1]

            return self.unhit_payoff.pay(st[-1], dates[-1]) * df[-1]

        else:
            raise TypeError("Barrier Type Error!")

    def pv(self, engine):
        return engine.calc_pv(self)
