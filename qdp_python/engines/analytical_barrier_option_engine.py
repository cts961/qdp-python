import numpy as np
from qdp_python.modules import BarrierType
from qdp_python.products import OptionType
from scipy.stats import norm


class CommonFactors:

    def __init__(self, process, option):
        self.process = process
        self.option = option

        self.T = self.process.day_counter.year_fraction(option.start_date, option.maturity_date)
        self.v_sqrt_t = process.v * np.sqrt(self.T)

        self.H = self.option.barrier.barrier_value

        self.mu = (process.r - process.q - 0.5 * process.v * process.v) / (process.v * process.v)
        self.l = np.sqrt(self.mu * self.mu + 2 * process.r / process.v / process.v)

        self.x1 = np.log(option.spot / option.strike) / self.v_sqrt_t + (1 + self.mu) * self.v_sqrt_t
        self.x2 = np.log(option.spot / self.H) / self.v_sqrt_t + (1 + self.mu) * self.v_sqrt_t
        self.y1 = np.log(self.H * self.H / option.spot / option.strike) / self.v_sqrt_t + (
                1 + self.mu) * self.v_sqrt_t
        self.y2 = np.log(self.H / option.spot) / self.v_sqrt_t + (1 + self.mu) * self.v_sqrt_t
        self.z = np.log(self.H / option.spot) / self.v_sqrt_t + self.l * self.v_sqrt_t

        self.d1 = (np.log(self.option.spot / self.option.strike) + (
                self.process.r - self.process.q + 0.5 * self.process.v * self.process.v) * self.T) / self.v_sqrt_t
        self.d2 = self.d1 - self.v_sqrt_t

    def factor_a(self, eta, phi):
        return phi * self.option.spot * np.exp(-self.process.q * self.T) * norm.cdf(phi * self.x1) \
               - phi * self.option.strike * np.exp(-self.process.r * self.T) * norm.cdf(
            phi * self.x1 - phi * self.v_sqrt_t)

    def factor_b(self, eta, phi):
        return phi * self.option.spot * np.exp(-self.process.q * self.T) * norm.cdf(phi * self.x2) \
               - phi * self.option.strike * np.exp(-self.process.r * self.T) * norm.cdf(
            phi * self.x2 - phi * self.v_sqrt_t)

    def factor_c(self, eta, phi):
        return phi * self.option.spot * np.exp(-self.process.q * self.T) * (self.H / self.option.spot) ** (
                2 * (self.mu + 1)) \
               * norm.cdf(eta * self.y1) - phi * self.option.strike * np.exp(-self.process.r * self.T) * (
                       self.H / self.option.spot) ** (2 * self.mu) \
               * norm.cdf(eta * self.y1 - eta * self.v_sqrt_t)

    def factor_d(self, eta, phi):
        return phi * self.option.spot * np.exp(-self.process.q * self.T) * (self.H / self.option.spot) ** (
                2 * (self.mu + 1)) \
               * norm.cdf(eta * self.y2) - phi * self.option.strike * np.exp(-self.process.r * self.T) * (
                       self.H / self.option.spot) ** (2 * self.mu) \
               * norm.cdf(eta * self.y2 - eta * self.v_sqrt_t)

    def factor_e(self, eta, phi):
        return self.option.rebate * np.exp(-self.process.r * self.T) * (
                norm.cdf(eta * self.x2 - eta * self.v_sqrt_t) - (self.H / self.option.spot) ** (
                2 * self.mu) * norm.cdf(eta * self.y2 - eta * self.v_sqrt_t))

    def factor_f(self, eta, phi):
        return self.option.rebate * (
                (self.H / self.option.spot) ** (self.mu + self.l) * norm.cdf(eta * self.z) + (
                self.H / self.option.spot) ** (self.mu - self.l) * norm.cdf(
            eta * self.z - 2 * eta * self.l * self.v_sqrt_t))

    def bs_call(self):
        return self.option.spot * np.exp(-self.process.q * self.T) * norm.cdf(self.d1) - self.option.strike * np.exp(
            -self.process.r * self.T) * norm.cdf(self.d2)

    def bs_put(self):
        return self.option.strike * np.exp(-self.process.r * self.T) * norm.cdf(-self.d2) - self.option.spot * np.exp(
            -self.process.q * self.T) * norm.cdf(-self.d1)


class AnalyticalBarrierOptionEngine:

    def __init__(self, process):
        self.process = process

    def calc_analytical_barrier_european_option(self, option):
        factors = CommonFactors(self.process, option)

        if option.barrier.barrier_type == BarrierType.UpOut:
            if option.spot >= option.barrier.barrier_value:
                return option.rebate
            else:
                if option.option_type == OptionType.Call:
                    eta = -1
                    phi = 1
                    if option.strike > option.barrier.barrier_value:
                        return factors.factor_f(eta, phi)
                    else:
                        return factors.factor_a(eta, phi) - factors.factor_b(eta, phi) + factors.factor_c(eta, phi) - \
                               factors.factor_d(eta, phi) + factors.factor_f(eta, phi)
                else:
                    eta = -1
                    phi = -1
                    if option.strike > option.barrier.barrier_value:
                        return factors.factor_b(eta, phi) - factors.factor_d(eta, phi) + factors.factor_f(eta, phi)
                    else:
                        return factors.factor_a(eta, phi) - factors.factor_c(eta, phi) + factors.factor_f(eta, phi)

        elif option.barrier.barrier_type == BarrierType.UpIn:
            if option.spot >= option.barrier.barrier_value:
                if option.option_type == OptionType.Call:
                    return factors.bs_call()
                else:
                    return factors.bs_put()
            else:
                if option.option_type == OptionType.Call:
                    eta = -1
                    phi = 1
                    if option.strike > option.barrier.barrier_value:
                        return factors.factor_a(eta, phi) + factors.factor_e(eta, phi)
                    else:
                        return factors.factor_b(eta, phi) - factors.factor_c(eta, phi) + factors.factor_d(eta, phi) \
                               + factors.factor_e(eta, phi)
                else:
                    eta = -1
                    phi = -1
                    if option.strike > option.barrier.barrier_value:
                        return factors.factor_a(eta, phi) - factors.factor_b(eta, phi) + factors.factor_d(eta, phi) \
                               + factors.factor_e(eta, phi)
                    else:
                        return factors.factor_c(eta, phi) + factors.factor_e(eta, phi)

        elif option.barrier.barrier_type == BarrierType.DownOut:
            if option.spot <= option.barrier.barrier_value:
                return option.rebate
            else:
                if option.option_type == OptionType.Call:
                    eta = 1
                    phi = 1
                    if option.strike > option.barrier.barrier_value:
                        return factors.factor_a(eta, phi) - factors.factor_c(eta, phi) + factors.factor_f(eta, phi)
                    else:
                        return factors.factor_b(eta, phi) - factors.factor_d(eta, phi) + factors.factor_f(eta, phi)
                else:
                    eta = 1
                    phi = -1
                    if option.strike > option.barrier.barrier_value:
                        return factors.factor_a(eta, phi) - factors.factor_b(eta, phi) + factors.factor_c(eta, phi) \
                               - factors.factor_d(eta, phi) + factors.factor_f(eta, phi)
                    else:
                        return factors.factor_f(eta, phi)

        elif option.barrier.barrier_type == BarrierType.DownIn:
            if option.spot <= option.barrier.barrier_value:
                if option.option_type == OptionType.Call:
                    return factors.bs_call()
                else:
                    return factors.bs_put()
            else:
                if option.option_type == OptionType.Call:
                    eta = 1
                    phi = 1
                    if option.strike > option.barrier.barrier_value:
                        return factors.factor_c(eta, phi) + factors.factor_e(eta, phi)
                    else:
                        return factors.factor_a(eta, phi) - factors.factor_b(eta, phi) + factors.factor_d(eta, phi) \
                               + factors.factor_e(eta, phi)
                else:
                    eta = 1
                    phi = -1
                    if option.strike > option.barrier.barrier_value:
                        return factors.factor_b(eta, phi) - factors.factor_c(eta, phi) + factors.factor_d(eta, phi) \
                               + factors.factor_e(eta, phi)
                    else:
                        return factors.factor_a(eta, phi) + factors.factor_e(eta, phi)
        else:
            raise TypeError("Barrier Type Error")


class AnalyticalDoubleBarrierOptionEngine:

    def __init__(self, process):
        self.process = process
        self.v2 = self.process.v * self.process.v
        self.b = self.process.r - self.process.q
        self.mu1 = 2 * self.b / self.v2 + 1
        self.mu2 = 0
        self.mu3 = self.mu1

    def calc_analytical_double_barrier_option(self, option):
        # use Ikeda and Kuintomo formula

        T = self.process.day_counter.year_fraction(option.start_date, option.maturity_date)
        L = option.barrier.barrier_value
        U = option.barrier.high_barrier_value
        S = option.spot
        X = option.strike

        engine = AnalyticalDoubleBarrierOptionEngine(self.process)
        factors = CommonFactors(self.process, option)
        if option.barrier.barrier_type == BarrierType.DoubleKnockOut:
            if S <= L or S >= U:
                return 0

            if option.option_type == OptionType.Call:
                return engine.up_out_down_out_call(T, L, U, S, X)
            else:
                return engine.up_out_down_out_put(T, L, U, S, X)
        elif option.barrier.barrier_type == BarrierType.DoubleKnockIn:
            if S <= L or S >= U:
                if option.option_type == OptionType.Call:
                    return factors.bs_call()
                else:
                    return factors.bs_put()

            if option.option_type == OptionType.Call:
                return factors.bs_call() - engine.up_out_down_out_call(T, L, U, S, X)
            else:
                return factors.bs_put() - engine.up_out_down_out_put(T, L, U, S, X)

    def up_out_down_out_call(self, T, L, U, S, X):
        v_sqrt_t = self.process.v * np.sqrt(T)
        F = U
        c = 0
        for n in range(-10, 11):
            d1 = (np.log(S * U ** (2 * n) / (X * L ** (2 * n))) + (self.b + self.v2 / 2) * T) / v_sqrt_t
            d2 = (np.log(S * U ** (2 * n) / (F * L ** (2 * n))) + (self.b + self.v2 / 2) * T) / v_sqrt_t
            d3 = (np.log(L ** (2 * n + 2) / (X * S * U ** (2 * n))) + (self.b + self.v2 / 2) * T) / v_sqrt_t
            d4 = (np.log(L ** (2 * n + 2) / (F * S * U ** (2 * n))) + (self.b + self.v2 / 2) * T) / v_sqrt_t

            c += S * np.exp((self.b - self.process.r) * T) * (
                        (U / L) ** (n * self.mu1) * (L / S) ** self.mu2 * (norm.cdf(d1) - norm.cdf(d2)) - (
                            L ** (n + 1) / S / (U ** n)) ** self.mu3 * (norm.cdf(d3) - norm.cdf(d4))) \
                - X * np.exp(-self.process.r * T) * (
                         (U / L) ** (n * (self.mu1-2)) * (L / S) ** self.mu2 * (norm.cdf(d1-v_sqrt_t) - norm.cdf(d2-v_sqrt_t)) - (
                            L ** (n + 1) / S / (U ** n)) ** (self.mu3-2) * (norm.cdf(d3-v_sqrt_t) - norm.cdf(d4-v_sqrt_t)))
        return c

    def up_out_down_out_put(self, T, L, U, S, X):
        v_sqrt_t = self.process.v * np.sqrt(T)
        E = L
        p = 0
        for n in range(-10, 11):
            y1 = (np.log(S*U**(2*n) / (E * L**(2*n))) + (self.b+self.v2 / 2) * T) / v_sqrt_t
            y2 = (np.log(S*U**(2*n) / (X * L**(2*n))) + (self.b+self.v2 / 2) * T) / v_sqrt_t
            y3 = (np.log(L**(2*n+2) / (E * S * U**(2*n))) + (self.b+self.v2 / 2) * T) / v_sqrt_t
            y4 = (np.log(L ** (2 * n + 2) / (X * S * U ** (2 * n))) + (self.b + self.v2 / 2) * T) / v_sqrt_t

            p += X * np.exp(- self.process.r * T) * (
                    (U / L) ** (n * (self.mu1-2)) * (L / S) ** self.mu2 * (norm.cdf(y1 - v_sqrt_t) - norm.cdf(y2 - v_sqrt_t)) -
                    (L ** (n + 1) / S / (U ** n)) ** (self.mu3-2) * (norm.cdf(y3 - v_sqrt_t) - norm.cdf(y4 - v_sqrt_t))) \
                - S * np.exp((self.b-self.process.r) * T) * (
                         (U / L) ** (n * self.mu1) * (L / S) ** self.mu2 * (norm.cdf(y1) - norm.cdf(y2)) -
                         (L ** (n + 1) / S / (U ** n)) ** self.mu3 * (norm.cdf(y3) - norm.cdf(y4)))
        return p




