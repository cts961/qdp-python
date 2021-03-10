from typing import List
from qdp_python import Date


class BarrierStatus(enumerate):
    Hit = 1
    UnHit = 0


class BarrierType(enumerate):
    UpOut = 1
    DownOut = 2
    UpIn = 3
    DownIn = 4
    DoubleKnockOut = 5
    DoubleKnockIn = 6


class BinaryType(enumerate):
    CashOrNothing = 1
    AssetOrNothing = 2
    UpOneTouch = 3
    UpNoTouch = 4
    DownOneTouch = 5
    DownNoTouch = 6
    DoubleOneTouch = 7
    DoubleNoTouch = 8




'''
create a dictionary according to the key, 
if the number of values is less then the number of keys, the last value will be repeated to pair with the keys
'''


def create_dict(keys, values) -> dict:
    gen_dict = {}
    if hasattr(keys, "__iter__") and hasattr(values, "__iter__"):
        if len(values) >= len(keys):
            for i in range(len(keys)):
                gen_dict[keys[i]] = values[i]
        else:
            for i in range(len(values)):
                gen_dict[keys[i]] = values[i]
            for i in range(len(values), len(keys)):
                gen_dict[keys[i]] = values[- 1]
    elif hasattr(keys, "__iter__"):
        for i in range(len(keys)):
            gen_dict[keys[i]] = values
    else:
        gen_dict[keys] = values

    return gen_dict


class Barrier:

    def __init__(self, observation_dates: List[Date], barrier_values, barrier_type: BarrierType,
                 high_barrier_values=None):
        self._barrier_dict = create_dict(observation_dates, barrier_values)
        self.barrier_type = barrier_type
        self._high_barrier_dict = create_dict(observation_dates, high_barrier_values)
        self.barrier_value = barrier_values
        self.high_barrier_value = high_barrier_values

    def is_hit(self, date: Date, spot: float) -> bool:
        barrier = self[date]
        try:
            self._high_barrier_dict[date]
        except KeyError:
            high_barrier = None
        else:
            high_barrier = self._high_barrier_dict[date]
        if barrier is not None:
            barrier_type = self.barrier_type
            if (barrier_type == BarrierType.UpOut or barrier_type == BarrierType.UpIn) and spot > barrier:
                return True
            if (barrier_type == BarrierType.DownOut or barrier_type == BarrierType.DownIn) and spot < barrier:
                return True
        if high_barrier is not None:
            barrier_type = self.barrier_type
            if (barrier_type == BinaryType.DoubleOneTouch or barrier_type == BinaryType.DoubleNoTouch) and (
                    spot > high_barrier or spot < barrier):
                return True
        return False

    @property
    def observation_dates(self):
        return list(self._barrier_dict)

    def __getitem__(self, date):
        try:
            return self._barrier_dict[date]
        except KeyError:
            return None



