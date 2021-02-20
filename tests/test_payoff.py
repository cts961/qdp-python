from unittest import TestCase

from modules.payoff import *


class TestPayoff(TestCase):
    def test_pay(self):
        # time independent payoff
        p1 = VanillaPayoff(PayoffType.Call, strike=1)

        p2 = BarrierPayoff(PayoffType.Put, BarrierType.DownOut, barrier=.9, strike=1.0)

        p3 = CashOrNothingPayoff(PayoffType.Call, strike=1.0, cash_amount=1.0)

        p4 = AssetOrNothingPayoff(PayoffType.Call, strike=1.0)

        self.assertAlmostEqual(p1.pay(1.1), 0.1, 10)
        self.assertAlmostEqual(p2.pay(0.95), 0.05, 10)
        self.assertAlmostEqual(p3.pay(1.1), 1, 10)
        self.assertAlmostEqual(p4.pay(1.1), 1.1, 10)


