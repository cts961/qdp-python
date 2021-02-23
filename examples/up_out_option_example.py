
from qdp_python import *


'''
=====================================================
option contract details:
 
option type: Up Out Call

start date = 2020/2/1
maturity date = 2021/2/1
strike = 100%
barrier : 120%
knock out as coupon , 20% annualized by Act365() convention
knock out observation : monthly

other variables:

spot = 100
valuation date = start date
volatility = 30%
risk free rate = 3%
dividend yield = 1%
=================================================================

Pricing result comparison details:


'''

# quad result:
# up out call: strike = 100, barrier = 120, ko_coupon = 10, pv = 2.86108382266224
# down out put: strike = 100, barrier = 80, ko_coupon = 10, pv = 3.39396650460264
# up in call: strike = 100, barrier = 120, ko_coupon = 0, pv = 12.3813109841292
# down in put: strike = 100, barrier = 80, ko_coupon = 0, pv = 8.89591466886489


calendar = China()
day_counter = Act365()
start_date = Date(2018, 1, 3)
maturity_date = Date(2019, 1, 3)
spot = 100

barrier_type = BarrierType.DownOut

# construct knock out coupon
coupon_rate = InterestRate(0.2)

coupon = Coupon(start_date, spot, coupon_rate)

observation_dates = [Date(2018, 2, 5), Date(2018, 3, 5), Date(2018, 4, 3), Date(2018, 5, 3),
                     Date(2018, 6, 4), Date(2018, 7, 3), Date(2018, 8, 3), Date(2018, 9, 3),
                     Date(2018, 10, 8), Date(2018, 11, 5), Date(2018, 12, 3), Date(2019, 1, 3)]

barrier = Barrier(observation_dates, 80, barrier_type)

hit_payoff = CashOrNothingPayoff(PayoffType.Put, barrier, coupon)

unhit_payoff = VanillaPayoff(PayoffType.Put, 100)

option = BarrierOption(spot,
                       start_date,
                       maturity_date,
                       barrier,
                       hit_payoff,
                       unhit_payoff
                       )
#
risk_free_rate = 0.03
dividend_yield = 0
volatility = 0.3

process = BlackScholesProcess(start_date, spot, risk_free_rate, dividend_yield, volatility, day_counter)

stime = time()
engine = MonteCarloEngine(process, 1000000)

npv = option.pv(engine)
print(time()-stime)
print(npv)

#
#
