from date.calendars import China
from modules.coupon import Coupon
from modules.payoff import *
from date.day_counter import *

# knock out definition
start_date = Date(2021, 1, 1)
ko_oberservation_dates = [Date(2021, 2, 19), Date(2021, 2, 18), Date(2021, 3, 18),
                          Date(2021, 4, 18), Date(2021, 5, 18),
                          Date(2021, 6, 18), Date(2021, 7, 18)]
ko_barrier_values = [1.0] * len(ko_oberservation_dates)

ko_barrier = Barrier(ko_oberservation_dates, ko_barrier_values, BarrierType.UpOut)

ki_oberservation_dates = [Date(2021, 2, 18), Date(2021, 2, 19), Date(2021, 3, 18),
                          Date(2021, 4, 18), Date(2021, 5, 1), Date(2021, 5, 18),
                          Date(2021, 6, 18), Date(2021, 7, 18)]
ki_barrier_values = [0.7] * len(ko_oberservation_dates)

ki_barriers = Barrier(ki_oberservation_dates, ki_barrier_values, BarrierType.DownIn)

ki_payoff = -VanillaPayoff(PayoffType.Put, 1.0)

ko_coupon = Coupon(0.2, Act365())

maturity_coupon = Coupon(0.05, Act365())

# give a stochastic path
# up out component

active_observation_dates = np.unique(ko_oberservation_dates + ki_oberservation_dates)
active_observation_dates.sort()


v = 0.3
r = 0.03
cal = Bus244(China())

drift = []
diffusion = []

df = []


valuation_date = Date(2021, 2, 18)
dt = cal.year_fraction(active_observation_dates[0], valuation_date)

drift.append((r - 0.5 * v * v) * dt)
diffusion.append(v * np.sqrt(dt))
df.append(np.exp(-r*dt))


for i in range(1, len(active_observation_dates)):
    dt = cal.year_fraction(active_observation_dates[i], active_observation_dates[i-1])

    drift.append((r-0.5*v*v)*dt)
    diffusion.append(v*np.sqrt(dt))

    df.append(np.exp(-r*Act365().year_fraction(valuation_date, active_observation_dates[i])))


# simulation start
eps = np.random.normal(0, 1, len(active_observation_dates))
logst = diffusion * eps + drift


st = np.exp(logst)


# one path simulation
def pv():
    ki_flag = 0
    for i in range(len(active_observation_dates)):
        current_date = active_observation_dates[i]
        if ko_barrier.is_hit(current_date, st[i]):
            return ko_coupon.pay(start_date, current_date) * df[i]
        if ki_barriers.is_hit(current_date, st[i]):
            ki_flag = 1.0

    last_date = active_observation_dates[-1]
    last_price = st[-1]

    mt = maturity_coupon.pay(start_date, last_date)

    return (ki_flag * ki_payoff.pay(last_price) + (1 - ki_flag) * mt) * df[-1]





