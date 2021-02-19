import numpy as np


def get_iid_eps(n_iterations, n_simulations):
    rand = np.zeros(shape=(n_iterations, n_simulations), dtype=float)
    for i in range(n_iterations):
        rand[i] = np.random.normal(0, 1, n_simulations)
    return rand.T


class MonteCarloEngine:

    def __init__(self, process):
        self.process = process

    def calc(self, option, n_simulations):
        valuation_date = self.process.reference_date
        cal = self.process.day_counter

        active_observation_dates = [valuation_date]
        active_observation_dates += [t for t in option.observation_dates if t > valuation_date]

        n_iterations = len(active_observation_dates)
        eps = get_iid_eps(n_iterations, n_simulations)

        drift = np.zeros(n_iterations)
        diffusion = np.zeros(n_iterations)
        df = np.zeros(n_iterations)

        drift[0] = 0
        diffusion[0] = 0
        df[0] = 1.0

        for i in range(1, len(active_observation_dates)):
            d1 = active_observation_dates[i - 1]
            d2 = active_observation_dates[i]
            t = cal.year_fraction(d1, d2)
            drift[i] = self.process.drift(t)
            diffusion[i] = self.process.diffusion(t)
            df[i] = self.process.discount_factor(t)

        logst = diffusion * eps + drift
        pv = np.zeros(n_simulations)
        for i in range(n_simulations):
            pv[i] = option.npv(active_observation_dates, np.exp(logst)[i], df)

        return np.average(pv)
