import numpy as np
import multiprocessing as mp
from joblib import Parallel, delayed
import torch
import QuantLib as ql


def get_iid_eps(n_iterations, n_simulations):
    rand = np.zeros(shape=(n_iterations, n_simulations), dtype=float)
    for i in range(n_iterations):
        rand[i] = np.random.normal(0, 1, n_simulations)
    return rand.T


def get_sobol_eps(n_iterations, n_simulations):
    sobol_array = np.zeros([n_simulations, n_iterations])
    sobol_engine = torch.quasirandom.SobolEngine(dimension=n_iterations)
    sobol_rand = sobol_engine.draw(n_simulations)

    invGauss = ql.MoroInverseCumulativeNormal()
    for i in range(n_simulations):
        for j in range(n_iterations):
            sobol_array[i][j] = invGauss(sobol_rand[i][j].item())
    return sobol_array


class MonteCarloEngine:

    def __init__(self, process, n_simulations):
        self.process = process
        self.n_simulations = n_simulations
        self.st = None

    def calc_pv(self, option):
        valuation_date = self.process.reference_date
        cal = self.process.day_counter
        n_simulations = self.n_simulations

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
            df[i] = self.process.discount_factor(cal.year_fraction(valuation_date, d2))

        rt = diffusion * eps + drift
        rt = rt.cumsum(axis=1)
        st = np.exp(rt) * self.process.spot

        # self.st = st

        def pv(s):
            return option.pv_by_path(active_observation_dates, s, df)

        num_cores = mp.cpu_count()

        results = Parallel(n_jobs=num_cores)(delayed(pv)(s) for s in st)
        return np.mean(results)

    def calc_path(self, option):
        valuation_date = self.process.reference_date
        cal = self.process.day_counter
        n_simulations = self.n_simulations

        active_observation_dates = [valuation_date]
        active_observation_dates += [t for t in option.observation_dates if t > valuation_date]
        n_iterations = len(active_observation_dates)
        eps = get_sobol_eps(n_iterations, n_simulations)

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
            df[i] = self.process.discount_factor(cal.year_fraction(valuation_date, d2))

        rt = diffusion * eps + drift
        rt = rt.cumsum(axis=1)
        st = np.exp(rt) * self.process.spot

        return st
