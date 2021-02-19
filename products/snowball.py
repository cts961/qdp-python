from modules.barrier import *


class Snowball:
    def __init__(self,
                 start_date,
                 ko_barrier,
                 ko_payoff_dict,
                 maturity_coupon,
                 ki_barrier=None,
                 ki_payoff=None,
                 ki_status=None):

        self.start_date = start_date
        self.ki_barrier = ki_barrier
        self.ki_payoff = ki_payoff
        self.ko_barrier = ko_barrier
        self.ko_payoff_dict = ko_payoff_dict
        self.maturity_coupon = maturity_coupon
        self.ki_flag = ki_status

    def npv(self, dates, st, df):
        ki_flag = self.ki_flag
        for t in range(len(dates)):
            d = dates[t]
            s = st[t]
            if self.ko_barrier.is_hit(d, s):
                return self.ko_payoff_dict[d](st[t]) * df[t]
            if self.ki_barrier is not None and ki_flag == 0 and self.ki_barrier.is_hit(d, st):
                ki_flag = BarrierStutus.Hit

        s = st[-1]

        mt = self.maturity_coupon

        return (self.ki_flag * self.ki_payoff.pay(s) + (1 - self.ki_flag) * mt) * df[-1]
