import time
import numpy as np
from scipy.stats import norm
import multiprocessing as mp


spot = 100

calc_day = 0

initialSpot = 100
ko_barrier = initialSpot * 1.0
coupon_rate = 0.20
ki_barrier = initialSpot * 0.70
ki_strike = initialSpot
days_in_a_year = 244
ko_observation_days = np.array([20, 42, 60, 81, 103, 124, 145, 162, 183, 205, 227, 249])

# compute the active ko observation days
ko_observation_days = ko_observation_days - calc_day
ko_observation_days = ko_observation_days[ko_observation_days > 0]

days_to_maturity = ko_observation_days[-1]
ki_observation_days = np.arange(1, days_to_maturity + 1)
# other parameters
r = 0.03
q = 0.0
v = 0.30

notional_principal = 100
dt = 1.0 / days_in_a_year


def mc_simulation(n):
    knock_in = False
    eps = norm.rvs(size=days_to_maturity)

    rt = np.array([0])
    rt = np.append(rt, (r - q - 0.5 * v * v) * dt + v * np.sqrt(dt) * eps)
    st = spot * np.exp(rt.cumsum())

    # knock out
    for i in range(len(ko_observation_days)):
        od = int(ko_observation_days[i])
        if st[od] > ko_barrier:
            return coupon_rate * (ko_observation_days[i] + calc_day) * dt * notional_principal * np.exp(
                -r * dt * ko_observation_days[i])

    # knock in
    if not knock_in:
        for i in range(len(ki_observation_days)):
            od = int(ki_observation_days[i])
            if st[od] < ki_barrier:
                knock_in = True
                break

    # terminal
    if knock_in:
        #
        return -max(ki_strike - st[-1], 0) / initialSpot * notional_principal * np.exp(-r * dt * days_to_maturity)
    else:
        return coupon_rate * (days_to_maturity + calc_day) * dt * notional_principal * np.exp(
            -r * dt * days_to_maturity)


if __name__ == "__main__":
    t_start = time.time()
    inputs = list(range(1000000))
    pool = mp.Pool(processes=mp.cpu_count())
    pool_outputs = pool.map(mc_simulation, inputs)
    pool.close()
    pool.join()
    mc_price = np.mean(pool_outputs, axis=0)
    t_end = time.time()

    print('mc Result - TIME: {}, MC Price: {}'.format(t_end - t_start, mc_price))
