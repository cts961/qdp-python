
# start_date = Date(2021, 1, 1)
# valuation_date = Date(2021, 2, 25)
#
# ko_oberservation_dates = [Date(2021, 2, 19), Date(2021, 2, 18), Date(2021, 3, 18),
#                           Date(2021, 4, 18), Date(2021, 5, 18),
#                           Date(2021, 6, 18), Date(2021, 7, 18)]
# ko_barrier_values = [1.0] * len(ko_oberservation_dates)
#
# ko_barrier = Barrier(ko_oberservation_dates, ko_barrier_values, BarrierType.UpOut)
#
# ko_coupon = Coupon(0.2, Act365())
#
# ko_payoff_dict = {}
# for d in ko_oberservation_dates:
#     ko_payoff_dict[d] = CashOrNothingPayoff(PayoffType.Call, ko_barrier[d], ko_coupon.pay(start_date, d))
#
# ki_oberservation_dates = [Date(2021, 2, 18), Date(2021, 2, 19), Date(2021, 3, 18),
#                           Date(2021, 4, 18), Date(2021, 5, 1), Date(2021, 5, 18),
#                           Date(2021, 6, 18), Date(2021, 7, 18)]
#
# ki_barrier_values = [0.7] * len(ko_oberservation_dates)
#
# ki_barrier = Barrier(ki_oberservation_dates, ki_barrier_values, BarrierType.DownIn)
#
# ki_payoff = -VanillaPayoff(PayoffType.Put, 1.0)
#
# # nki nko definition
# maturity_coupon = Coupon(0.05, Act365())
#
# # give a stochastic path
# # up out component
