import numpy as np


class ConstantVolatility:
    def __init__(self, vol, day_counter):
        self._vol = vol
        self._day_counter = day_counter

    def variance(self, d1, d2):
        t = self._day_counter.year_fraction(d1, d2)
        return self._vol * self._vol * t

    def vol(self, d1, d2):
        return np.sqrt(self.variance(d1, d2))