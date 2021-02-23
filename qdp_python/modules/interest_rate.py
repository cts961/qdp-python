import numpy as np

from qdp_python import Act365


class Compounding(enumerate):
    Simple = 1
    Compounded = 2
    Continuous = 3


class Frequency(enumerate):
    NoFrequency = -1
    Once = 0
    Annually = 1
    Semiannually = 2
    EveryFourthMonth = 3
    Quarterly = 4
    Bimonthly = 6
    Monthly = 12
    EveryFourthWeek = 13
    Biweekly = 26
    Weekly = 52
    Daily = 365
    OtherFrequency = 999


class InterestRate:
    def __init__(self, rate, day_counter=Act365(), compounding=Compounding.Simple, frequency=Frequency.Annually):
        self._rate = rate
        self._day_counter = day_counter
        self._compounding = compounding
        self._frequency = frequency

    def compound_factor(self, d1, d2):
        t = self._day_counter.year_fraction(d1, d2)
        if self._compounding == Compounding.Simple:
            return 1 + self._rate * t
        if self._compounding == Compounding.Compounded:
            return np.pow(1 + self._rate / self._frequency, self._frequency * t)
        if self._compounding == Compounding.Continuous:
            return np.exp(self._rate * t)
        else:
            raise TypeError("Compounding type not supported")

    def discount_factor(self, d1, d2):
        return 1 / self.compound_factor(d1, d2)


class Coupon:
    def __init__(self, reference_date, principal_amount, rate: InterestRate, day_counter=None):
        self._principal_amount = principal_amount
        self._reference_date = reference_date
        self._rate = rate
        self._day_counter = day_counter

    @property
    def principal_amount(self):
        return self._principal_amount

    @principal_amount.setter
    def principal_amount(self, value):
        self._principal_amount = value

    def __getitem__(self, date):
        return (self._rate.compound_factor(self._reference_date, date) - 1) * self._principal_amount

    def pay_schedule(self, dates):
        if hasattr(dates, "__iter__"):
            yields = {}
            for date in dates:
                yields[date] = self[date]
            return yields
        else:
            return {dates: self[dates]}


