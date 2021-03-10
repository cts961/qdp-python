from qdp_python import *

# the complete guide page 175

calendar = China()
day_counter = Bus244()
# T = 0.75Y
start_date = Date(2018, 1, 3)
maturity_date = Date(2018, 10, 9)
spot = 100

barrier_type = BinaryType.CashOrNothing

barrier = Barrier([], None, barrier_type)

option = BarrierOption(spot,
                       start_date,
                       maturity_date,
                       barrier,
                       None,
                       None,
                       strike=80,
                       rebate=10,
                       option_type=OptionType.Put)

risk_free_rate = 0.06
dividend_yield = 0.06
volatility = 0.35

process = BlackScholesProcess(start_date, spot, risk_free_rate, dividend_yield, volatility, day_counter)

engine = AnalyticalBinaryOptionEngine(process)

pv = engine.calc_analytical_binary_european_option(option)

print(pv)



