from qdp_python import *


'''
=====================================================
option contract details:
 
option type: Up In Call

start date = 2018/1/3
maturity date = 2019/1/3
strike = 100%
barrier : 120%

knock in as call 
knock in observation : monthly
never knock in as coupon, 0%

other variables:

spot = 100
valuation date = start date
volatility = 30%
risk free rate = 3%
dividend yield = 1%
=================================================================

Pricing result comparison details:
quad pv = 11.771861580065
mc pv = 11.79891769674576
relative error = (quad pv / mc pv - 1) * 100 = -0.23%

'''


calendar = China()
day_counter = Bus244()
start_date = Date(2018, 1, 3)
maturity_date = Date(2019, 1, 3)
spot = 100

barrier_type = BarrierType.UpIn

# construct never knock in coupon
coupon_rate = InterestRate(0.0)
coupon = Coupon(start_date, spot, coupon_rate)

observation_dates = [Date(2018, 2, 5), Date(2018, 3, 5), Date(2018, 4, 3), Date(2018, 5, 3),
                     Date(2018, 6, 4), Date(2018, 7, 3), Date(2018, 8, 3), Date(2018, 9, 3),
                     Date(2018, 10, 8), Date(2018, 11, 5), Date(2018, 12, 3), Date(2019, 1, 3)]

barrier = Barrier(observation_dates, 120, barrier_type)

hit_payoff = VanillaPayoff(PayoffType.Call, 100)

unhit_payoff = CashOrNothingPayoff(PayoffType.Put, barrier, coupon)

option = BarrierOption(spot,
                       start_date,
                       maturity_date,
                       barrier,
                       hit_payoff,
                       unhit_payoff)

risk_free_rate = 0.03
dividend_yield = 0.01
volatility = 0.3

process = BlackScholesProcess(start_date, spot, risk_free_rate, dividend_yield, volatility, day_counter)

engine = MonteCarloEngine(process, 100000)

npv = option.pv(engine)
print(npv)


