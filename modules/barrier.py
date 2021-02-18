from typing import List

from date.date import Date
from modules.payoff import Payoff


class BarrierType(enumerate):
    UpOut = 1
    DownOut = 2
    UpIn = 3
    DownIn = 4


class Barrier:
    def __init__(self, observation_dates: List[Date], barriers: List[float], barrier_type: BarrierType):
        self.observation_dates = observation_dates
        self.barriers = barriers
        self.barrier_dict = dict(zip(observation_dates, barriers))
        self.barrier_type = barrier_type

    def is_hit(self, date: Date, spot: float) -> bool:
        if date in self.barrier_dict.keys():
            barrier = self.barrier_dict[date]
            barrier_type = self.barrier_type
            if (barrier_type == BarrierType.UpOut or barrier_type == BarrierType.UpIn) and spot > barrier:
                return True
            if (barrier_type == BarrierType.DownOut or barrier_type == BarrierType.DownIn) and spot < barrier:
                return True
        return False


