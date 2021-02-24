from unittest import TestCase

from qdp_python import *


class TestBarrier(TestCase):
    def test_is_hit(self):
        observation_dates = [Date(2021, 2, 17), Date(2021, 2, 18),
                             Date(2021, 3, 18), Date(2021, 4, 18),
                             Date(2021, 5, 18), Date(2021, 6, 18),
                             Date(2021, 7, 18), Date(2021, 8, 18)]
        barrier_values = [1., 2, 3.]
        barrier = Barrier(observation_dates, barrier_values, BarrierType.DownOut)

        self.assertTrue(barrier.is_hit(observation_dates[0], 0.9))
        self.assertTrue(barrier.is_hit(observation_dates[1], 1.5))
        self.assertTrue(barrier.is_hit(observation_dates[2], 2.1))
        self.assertTrue(barrier.is_hit(observation_dates[3], 2.1))

    def test_is_hit_for_double_barrier(self):
        observation_dates = [Date(2021, 2, 17), Date(2021, 2, 18),
                             Date(2021, 3, 18), Date(2021, 4, 18),
                             Date(2021, 5, 18), Date(2021, 6, 18),
                             Date(2021, 7, 18), Date(2021, 8, 18)]
        barrier_values = [1, 2, 3]
        high_barrier_values = [2, 3, 4]
        barrier = Barrier(observation_dates, barrier_values, BarrierType.DoubleOneTouch, high_barrier_values)

        self.assertTrue(barrier.is_hit(observation_dates[0], 0.9))
        self.assertTrue(barrier.is_hit(observation_dates[1], 3.1))


