from unittest import TestCase

from date_utils.date import Date
from modules.barrier import Barrier, BarrierType, create_dict


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


class Test(TestCase):
    def test_create_dict(self):
        dict1 = create_dict(Date(2021, 2, 21), 1.0)
        self.assertEqual(dict1[Date(2021, 2, 21)], 1.0)

        dict2 = create_dict([Date(2021, 2, 21), Date(2021, 2, 22)], 1.0)
        self.assertEqual(dict2[Date(2021, 2, 22)], 1.0)

        dict3 = create_dict([Date(2021, 2, 21), Date(2021, 2, 22)], [1.0, 2.0])
        self.assertEqual(dict3[Date(2021, 2, 22)], 2.0)

        dict4 = create_dict([Date(2021, 2, 21), Date(2021, 2, 22)], [1.0, 2.0, 3.0])
        self.assertEqual(dict4[Date(2021, 2, 22)], 2.0)

        dict5 = create_dict([Date(2021, 2, 21), Date(2021, 2, 22)], [1.0])
        self.assertEqual(dict5[Date(2021, 2, 22)], 1.0)


