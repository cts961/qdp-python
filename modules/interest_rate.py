import numpy as np


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
    def __init__(self, rate, day_counter, compounding, frequency=Frequency.Annually):
        self._rate = rate
        self._day_counter = day_counter
        self._compounding = compounding
        self._frequency = frequency

    def compound_factor(self, d1, d2):
        t = self._day_counter.year_fraction(d1, d2)
        if self._compounding == Compounding.Simple:
            return (1+self._rate)*t
        if self._compounding == Compounding.Compounded:
            return np.pow(1+self._rate/self._frequency, self._frequency * t)
        if self._compounding == Compounding.Continuous:
            return np.exp(self._rate * t)
        else:
            raise TypeError("Compounding type not surpported")

    def discount_factor(self, d1, d2):
        t = self._day_counter.year_fraction(d1, d2)
        return 1/self.compound_factor(d1, d2)


