import numpy as np


# a general geometric brownian motion is like this
# log(s(t)) = log(s(0))  + drift(t) + diffusion(t)* w
# in blackscholes process, w follows gauss distriubition

class BlackScholesProcess:
    def __init__(self, reference_date, spot, r, q, v, day_counter):
        self.reference_date = reference_date
        self.spot = spot
        self.r = r
        self.q = q
        self.v = v
        self.day_counter = day_counter

    def drift(self, t):
        return (self.r - self.q - 0.5 * self.v * self.v) * t

    def diffusion(self, t):
        return self.v * np.srt(t)

    def discount_factor(self, t):
        return np.exp(-self.r * t)
