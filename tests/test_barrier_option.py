from unittest import TestCase

from qdp_python import *


class TestBarrierOption(TestCase):
    def test_up_out_pv_by_path(self):
        """
        test up out call option pv by path

        params: barrier = 120, coupon = [10, 11, 12, 13], strike = 100

        path1: knock out on the third observation day, pay coupon, pv should be 12
        path2: never knock out, pay a call, pv should be Max(st[-1]-100, 0) = 8

        """
        spot = 100
        strike = 100

        observation_dates = [Date(2018, 2, 5), Date(2018, 3, 5), Date(2018, 4, 3), Date(2018, 5, 3)]
        start_date = observation_dates[0]
        maturity_date = observation_dates[-1]

        coupon = {observation_dates[0]: 10, observation_dates[1]: 11, observation_dates[2]: 12,
                  observation_dates[3]: 13}

        hit_payoff = CashOrNothingPayoff(PayoffType.Call, 120, coupon)
        unhit_payoff = VanillaPayoff(PayoffType.Call, strike)

        barrier = Barrier(observation_dates, 120, BarrierType.UpOut)

        option = BarrierOption(spot,
                               start_date,
                               maturity_date,
                               barrier,
                               hit_payoff,
                               unhit_payoff)
        df = [1, 1, 1, 1]

        # path1:  knock out on the third observation day, pay coupon = 12
        st1 = [100, 113, 121, 130]
        self.assertTrue(BarrierOption.pv_by_path(option, observation_dates, st1, df), 12)

        # path2: never knock out, pay a call = 108 - 100 = 8
        st2 = [100, 80, 90, 108]
        self.assertTrue(BarrierOption.pv_by_path(option, observation_dates, st2, df), 8)

    def test_down_out_pv_by_path(self):
        """
        test down out put option pv by path

        params: barrier = 80, coupon = [10, 11, 12, 13], strike = 100

        path1: knock out on the fourth observation day, pay coupon, pv should be 13
        path2: never knock out, pay a put, pv should be Max(100 - st[-1], 0) = 2

        """
        spot = 100
        strike = 100

        observation_dates = [Date(2018, 2, 5), Date(2018, 3, 5), Date(2018, 4, 3), Date(2018, 5, 3)]
        start_date = observation_dates[0]
        maturity_date = observation_dates[-1]

        coupon = {observation_dates[0]: 10, observation_dates[1]: 11, observation_dates[2]: 12,
                  observation_dates[3]: 13}

        hit_payoff = CashOrNothingPayoff(PayoffType.Put, 80, coupon)
        unhit_payoff = VanillaPayoff(PayoffType.Put, strike)

        barrier = Barrier(observation_dates, 80, BarrierType.DownOut)

        option = BarrierOption(spot,
                               start_date,
                               maturity_date,
                               barrier,
                               hit_payoff,
                               unhit_payoff)
        df = [1, 1, 1, 1]

        # path1: knock out on the fourth observation day, pay coupon = 13
        st1 = [100, 90, 85, 70]
        self.assertTrue(BarrierOption.pv_by_path(option, observation_dates, st1, df), 13)

        # path2: never knock out, pay put = 100 - 98 = 2
        st2 = [100, 85, 90, 98]
        self.assertTrue(BarrierOption.pv_by_path(option, observation_dates, st2, df), 2)

    def test_up_in_pv_by_path(self):
        """
        test up in call option pv by path

        params: barrier = 120, coupon = 15, strike = 100

        path1: knock in, pay a call, pv should be Max(st[-1] - 100, 0) = 30
        path2: never knock in, pay coupon, pv should be coupon = 15

        """
        spot = 100
        strike = 100
        coupon = 15
        hit_payoff = VanillaPayoff(PayoffType.Call, strike)
        unhit_payoff = CashOrNothingPayoff(PayoffType.Put, 120, coupon)

        observation_dates = [Date(2018, 2, 5), Date(2018, 3, 5), Date(2018, 4, 3), Date(2018, 5, 3)]
        start_date = observation_dates[0]
        maturity_date = observation_dates[-1]

        barrier = Barrier(observation_dates, 120, BarrierType.UpIn)

        option = BarrierOption(spot,
                               start_date,
                               maturity_date,
                               barrier,
                               hit_payoff,
                               unhit_payoff)
        df = [1, 1, 1, 1]

        # path1: knock in, pay a call, pv = 130 - 100 = 30
        st1 = [100, 105, 121, 130]
        self.assertTrue(BarrierOption.pv_by_path(option, observation_dates, st1, df), 30)

        # path2: never knock in, pay coupon = 15
        st2 = [100, 80, 90, 108]
        self.assertTrue(BarrierOption.pv_by_path(option, observation_dates, st2, df), 15)

    def test_down_in_pv_by_path(self):
        """
        test down in put option pv by path

        params: barrier = 80, coupon = 15, strike = 100

        path1: knock in, pay a put, pv should be Max(100 - st[-1], 0) = 30
        path2: never knock in, pay coupon, pv should be coupon = 15

        """
        spot = 100
        strike = 100
        coupon = 15
        hit_payoff = VanillaPayoff(PayoffType.Put, strike)
        unhit_payoff = CashOrNothingPayoff(PayoffType.Call, 80, coupon)

        observation_dates = [Date(2018, 2, 5), Date(2018, 3, 5), Date(2018, 4, 3), Date(2018, 5, 3)]
        start_date = observation_dates[0]
        maturity_date = observation_dates[-1]

        barrier = Barrier(observation_dates, 80, BarrierType.DownIn)

        option = BarrierOption(spot,
                               start_date,
                               maturity_date,
                               barrier,
                               hit_payoff,
                               unhit_payoff)
        df = [1, 1, 1, 1]
        # path1: knock in, pay a put, pv = 100 - 70 = 30
        st1 = [100, 90, 85, 70]
        self.assertTrue(BarrierOption.pv_by_path(option, observation_dates, st1, df), 30)
        # path2: never knock in, pay coupon = 15
        st2 = [100, 85, 90, 101]
        self.assertTrue(BarrierOption.pv_by_path(option, observation_dates, st2, df), 15)

    def test_double_out_pv_by_path(self):
        """
        test double out call option pv by path

        params: barrier = 80, high_barrier = 120, coupon = 15, strike = 100

        path1: knock down out on the fourth observation day, pv should be coupon = 13
        path2: knock up out on the third observation day, pv should be coupon = 12
        path3: never knock out, pay a call, pv should be Max(st[-1] - 100) = 1

        """
        spot = 100
        strike = 100

        observation_dates = [Date(2018, 2, 5), Date(2018, 3, 5), Date(2018, 4, 3), Date(2018, 5, 3)]
        start_date = observation_dates[0]
        maturity_date = observation_dates[-1]

        coupon = {observation_dates[0]: 10, observation_dates[1]: 11, observation_dates[2]: 12,
                  observation_dates[3]: 13}

        hit_payoff = CashOrNothingPayoff(PayoffType.Call, 120, coupon) + CashOrNothingPayoff(PayoffType.Put, 80, coupon)
        unhit_payoff = VanillaPayoff(PayoffType.Call, strike)

        barrier = Barrier(observation_dates, 80, BarrierType.DoubleOneTouch, high_barrier_values=120)

        option = BarrierOption(spot,
                               start_date,
                               maturity_date,
                               barrier,
                               hit_payoff,
                               unhit_payoff)
        df = [1, 1, 1, 1]

        # path1: knock down out on the fourth observation day, coupon = 13
        st1 = [100, 90, 85, 70]
        self.assertTrue(BarrierOption.pv_by_path(option, observation_dates, st1, df), 13)

        # path2: knock up out on the third observation day, coupon = 12
        st2 = [100, 110, 121, 119]
        self.assertTrue(BarrierOption.pv_by_path(option, observation_dates, st2, df), 12)

        # path2: never knock out, pay a call, pv = 101 - 100 = 1
        st3 = [100, 85, 90, 101]
        self.assertTrue(BarrierOption.pv_by_path(option, observation_dates, st3, df), 1)

    def test_double_In_pv_by_path(self):
        """
        test double In Put option pv by path

        params: barrier = 80, high_barrier = 120, coupon = 15, strike = 100

        path1: knock down In on the fourth observation day, pv should be Max(100 - st[-1], 0)
        path2: knock up In on the third observation day, pv should be Max(100 - st[-1], 0)
        path3: never knock In, pay a coupon

        """
        spot = 100
        strike = 100

        observation_dates = [Date(2018, 2, 5), Date(2018, 3, 5), Date(2018, 4, 3), Date(2018, 5, 3)]
        start_date = observation_dates[0]
        maturity_date = observation_dates[-1]

        coupon = 15

        unhit_payoff = CashOrNothingPayoff(PayoffType.Put, 120, coupon) + CashOrNothingPayoff(PayoffType.Call, 80,
                                                                                              coupon)
        hit_payoff = VanillaPayoff(PayoffType.Put, strike)

        barrier = Barrier(observation_dates, 80, BarrierType.DoubleNoTouch, high_barrier_values=120)

        option = BarrierOption(spot,
                               start_date,
                               maturity_date,
                               barrier,
                               hit_payoff,
                               unhit_payoff)
        df = [1, 1, 1, 1]

        # path1: knock down In on the fourth observation day, pv = 100 - 70 = 30
        st1 = [100, 90, 85, 70]
        self.assertTrue(BarrierOption.pv_by_path(option, observation_dates, st1, df), 30)

        # path2: knock up In on the third observation day, pv = 100 - 95 = 5
        st2 = [100, 110, 121, 95]
        self.assertTrue(BarrierOption.pv_by_path(option, observation_dates, st2, df), 5)

        # path3: never knock In, pay a coupon = 15
        st3 = [100, 85, 90, 101]
        self.assertTrue(BarrierOption.pv_by_path(option, observation_dates, st3, df), 15)
