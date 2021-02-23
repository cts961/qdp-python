from time import time

from qdp_python import *

calendar = China()
day_counter = Bus244()
start_date = Date(2021, 2, 22)
maturity_date = Date(2022, 2, 22)
initial_spot = 100

coupon_rate = InterestRate(0.2, day_counter)

ko_coupon = Coupon(start_date, initial_spot, coupon_rate)
maturity_coupon = Coupon(start_date, initial_spot, coupon_rate)

ko_observation_dates = [Date(2021, 3, 22), Date(2021, 4, 22), Date(2021, 5, 21),
                        Date(2021, 6, 22), Date(2021, 7, 22), Date(2021, 8, 20),
                        Date(2021, 9, 22), Date(2021, 10, 22), Date(2021, 11, 22),
                        Date(2021, 12, 22), Date(2022, 1, 22), Date(2022, 2, 22)]

ko_barrier = Barrier(ko_observation_dates, [100, 101, 102], BarrierType.UpOut)


ko_payoff = CashOrNothingPayoff(PayoffType.Call, ko_barrier, ko_coupon)

ki_observation_dates = []

d = start_date
while d <= maturity_date:
    if calendar.is_business_day(d):
        ki_observation_dates.append(d)
    d = d.next_day()


ki_barrier = Barrier(ki_observation_dates, 70, BarrierType.DownIn)
# we can treat the participation rate as the annualizartion factor
ki_payoff = -VanillaPayoff(PayoffType.Put, 100)

option = Snowball(initial_spot=initial_spot,
                  start_date=start_date,
                  maturity_date=maturity_date,
                  ko_barrier=ko_barrier,
                  ko_payoff=ko_payoff,
                  maturity_coupon=maturity_coupon,
                  ki_barrier=ki_barrier,
                  ki_payoff=ki_payoff,
                  ki_status=BarrierStatus.UnHit)

risk_free_rate = 0.03
dividend_yield = 0
volatility = 0.3

process = BlackScholesProcess(start_date, initial_spot, risk_free_rate, dividend_yield, volatility, day_counter)

stime = time()
engine = MonteCarloEngine(process, 100000)

npv = option.pv(engine)
print(npv)

