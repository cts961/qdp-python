from datetime import datetime, timedelta


class Date:
    def __init__(self, year: int, month: int, day: int):
        self.year = year
        self.month = month
        self.day = day

    def datetime(self):
        return datetime(self.year, self.month, self.day)

    def weekday(self):
        return self.datetime().weekday()

    def __sub__(self, other):
        return (self.datetime() - other.datetime()).days

    def __lt__(self, other):
        return self.datetime() < other.datetime()

    def __gt__(self, other):
        return self.datetime() > other.datetime()

    def __eq__(self, other):
        return self.datetime() == other.datetime()

    def __le__(self, other):
        return self.datetime() <= other.datetime()

    def __hash__(self):
        return hash(self.datetime())

    def __repr__(self):
        return "Date(" + str(self.year) + ", " + str(self.month) + ", " + str(self.day) + ")"

    def previous_day(self):
        dt = timedelta(days=-1)
        d = self.datetime()
        d += dt
        return Date(d.year, d.month, d.day)

    def next_day(self):
        dt = timedelta(days=1)
        d = self.datetime()
        d += dt
        return Date(d.year, d.month, d.day)
