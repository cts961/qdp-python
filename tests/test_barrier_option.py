from unittest import TestCase

from qdp_python import *


class TestBarrier(TestCase):
    def test_up_out_pv_by_path(self):
        spot = 100
        strike = 100
        coupon = 15
        hit_payoff = CashOrNothingPayoff(PayoffType.Call, 120, coupon)
        unhit_payoff = VanillaPayoff(PayoffType.Call, strike)

        observation_dates = [Date(2018, 2, 5), Date(2018, 3, 5), Date(2018, 4, 3), Date(2018, 5, 3)]
        start_date = observation_dates[0]
        maturity_date = observation_dates[-1]

        barrier = Barrier(observation_dates, 120, BarrierType.UpOut)

        st1 = [100, 105, 121, 130]
        df = [1, 1, 1, 1]
        option = BarrierOption(spot,
                               start_date,
                               maturity_date,
                               barrier,
                               hit_payoff,
                               unhit_payoff)
        self.assertTrue(BarrierOption.pv_by_path(option, observation_dates, st1, df), 15)
        st2 = [100, 80, 90, 108]
        self.assertTrue(BarrierOption.pv_by_path(option, observation_dates, st2, df), 8)

    def test_down_out_pv_by_path(self):
        spot = 100
        strike = 100
        coupon = 15
        hit_payoff = CashOrNothingPayoff(PayoffType.Put, 80, coupon)
        unhit_payoff = VanillaPayoff(PayoffType.Put, strike)

        observation_dates = [Date(2018, 2, 5), Date(2018, 3, 5), Date(2018, 4, 3), Date(2018, 5, 3)]
        start_date = observation_dates[0]
        maturity_date = observation_dates[-1]

        barrier = Barrier(observation_dates, 80, BarrierType.DownOut)

        st1 = [100, 90, 85, 70]
        df = [1, 1, 1, 1]
        option = BarrierOption(spot,
                               start_date,
                               maturity_date,
                               barrier,
                               hit_payoff,
                               unhit_payoff)
        self.assertTrue(BarrierOption.pv_by_path(option, observation_dates, st1, df), 15)
        st2 = [100, 85, 90, 98]
        self.assertTrue(BarrierOption.pv_by_path(option, observation_dates, st2, df), 2)

    def test_up_in_pv_by_path(self):
        spot = 100
        strike = 100
        coupon = 15
        hit_payoff = VanillaPayoff(PayoffType.Call, strike)
        unhit_payoff = CashOrNothingPayoff(PayoffType.Put, 120, coupon)

        observation_dates = [Date(2018, 2, 5), Date(2018, 3, 5), Date(2018, 4, 3), Date(2018, 5, 3)]
        start_date = observation_dates[0]
        maturity_date = observation_dates[-1]

        barrier = Barrier(observation_dates, 120, BarrierType.UpIn)

        st1 = [100, 105, 121, 130]
        df = [1, 1, 1, 1]
        option = BarrierOption(spot,
                               start_date,
                               maturity_date,
                               barrier,
                               hit_payoff,
                               unhit_payoff)
        self.assertTrue(BarrierOption.pv_by_path(option, observation_dates, st1, df), 30)
        st2 = [100, 80, 90, 108]
        self.assertTrue(BarrierOption.pv_by_path(option, observation_dates, st2, df), 15)

    def test_down_in_pv_by_path(self):
        spot = 100
        strike = 100
        coupon = 15
        hit_payoff = VanillaPayoff(PayoffType.Put, strike)
        unhit_payoff = CashOrNothingPayoff(PayoffType.Call, 80, coupon)

        observation_dates = [Date(2018, 2, 5), Date(2018, 3, 5), Date(2018, 4, 3), Date(2018, 5, 3)]
        start_date = observation_dates[0]
        maturity_date = observation_dates[-1]

        barrier = Barrier(observation_dates, 80, BarrierType.DownIn)

        st1 = [100, 90, 85, 70]
        df = [1, 1, 1, 1]
        option = BarrierOption(spot,
                               start_date,
                               maturity_date,
                               barrier,
                               hit_payoff,
                               unhit_payoff)
        self.assertTrue(BarrierOption.pv_by_path(option, observation_dates, st1, df), 30)
        st2 = [100, 85, 90, 101]
        self.assertTrue(BarrierOption.pv_by_path(option, observation_dates, st2, df), 15)