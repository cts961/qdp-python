class Coupon:
    def __init__(self, coupon_rate, day_counter):
        self.coupon_rate = coupon_rate
        self.day_counter = day_counter

    def pay(self, from_date, to_date):
        return self.coupon_rate * self.day_counter.year_fraction(from_date, to_date)