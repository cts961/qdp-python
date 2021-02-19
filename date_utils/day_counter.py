from date_utils.calendars import China


class DayCounter:
    def __init__(self, calendar=China()):
        self.calendar = calendar

    def year_fraction(self, from_date, to_date):
        pass


class Act365(DayCounter):
    def year_fraction(self, from_date, to_date):
        if from_date < to_date:
            return (to_date - from_date) / 365.0
        return (from_date - to_date)/365.0


class Bus244(DayCounter):
    def year_fraction(self, from_date, to_date):
        if from_date > to_date:
            return self.calendar.business_days_between(to_date, from_date) / 244.0
        return self.calendar.business_days_between(from_date, to_date) / 244.0
