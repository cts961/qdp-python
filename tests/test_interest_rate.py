from unittest import TestCase

from qdp_python import *


class TestCoupon(TestCase):
    def test_coupon(self):
        rate = InterestRate(0.2, Act365(), Compounding.Simple)
        bond = Coupon(Date(2021, 2, 21), 100, rate)
        self.assertAlmostEqual(bond[Date(2022, 2, 21)], 20.0, places=10)
