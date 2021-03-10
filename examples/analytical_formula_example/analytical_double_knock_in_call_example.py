from qdp_python import *


calendar = China()
day_counter = Bus244()
# T = 0.5Y
start_date = Date(2018, 1, 3)
maturity_date = Date(2018, 7, 6)
spot = 100

barrier_type = BarrierType.DoubleKnockIn

barrier = Barrier([], 90, barrier_type, 110)

option = BarrierOption(spot,
                       start_date,
                       maturity_date,
                       barrier,
                       None,
                       None,
                       strike=100,
                       option_type=OptionType.Call)

risk_free_rate = 0.1
dividend_yield = 0.0
volatility = 0.25

process = BlackScholesProcess(start_date, spot, risk_free_rate, dividend_yield, volatility, day_counter)

engine = AnalyticalDoubleBarrierOptionEngine(process)

pv = engine.calc_analytical_double_barrier_option(option)

print(pv)



