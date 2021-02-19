from typing import List
from date_utils.date import Date


class BarrierStutus(enumerate):
    Hit = 1
    UnHit = 0


class BarrierType(enumerate):
    UpOut = 1
    DownOut = 2
    UpIn = 3
    DownIn = 4


class Barrier:

    def __init__(self, observation_dates: List[Date], barriers: List[float], barrier_type: BarrierType):
        self._observation_dates = observation_dates
        self._barriers = barriers
        self._barrier_dict = dict(zip(observation_dates, barriers))
        self._barrier_type = barrier_type

    def is_hit(self, date: Date, spot: float) -> bool:
        barrier = self[date]
        if barrier is not None:
            barrier_type = self._barrier_type
            if (barrier_type == BarrierType.UpOut or barrier_type == BarrierType.UpIn) and spot > barrier:
                return True
            if (barrier_type == BarrierType.DownOut or barrier_type == BarrierType.DownIn) and spot < barrier:
                return True
        return False

    def __getitem__(self, date):
        try:
            return self._barrier_dict[date]
        except KeyError:
            return None

