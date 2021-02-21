from unittest import TestCase

from date_utils.date import Date
from date_utils.day_counter import Act365
from modules.interest_rate import InterestRate, Compounding, Yield


class TestCallableBond(TestCase):
    def test_yield(self):
        rate = InterestRate(0.2, Act365(), Compounding.Simple)
        bond = Yield(100, rate, Date(2021, 2, 21))

        self.assertTrue(bond[Date(2022, 2, 21)], 20.0)
