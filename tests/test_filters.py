import unittest
from datetime import datetime
from datetime import timedelta
from clock_framework.filters import *
from clock_framework.task import Task
from clock_framework.task import Period

class TestDateFilter(unittest.TestCase):
    def test__task_today__returns_true(self):
        filter = DateFilter(datetime.today())
        task = Task('Test', datetime.now())
        self.assertTrue(filter.is_valid(task))

    def test__task_yesterday__returns_false(self):
        filter = DateFilter(datetime.today() - timedelta(days=1))
        task = Task('Test', datetime.now())
        self.assertFalse(filter.is_valid(task))

    def test__task_two_different_periods__returns_task_with_single_period(self):
        filter = DateFilter(datetime.today())
        task = Task('Test', datetime.today() - timedelta(days=1))
        task.finish(datetime.now() - timedelta(days=1))
        task.periods.append(Period(datetime.now()))

        result = filter.get_task(task)
        self.assertEqual(len(result.periods), 1)
        self.assertEqual(result.periods[0].start.date(), datetime.today().date())

class TestPeriodFilter(unittest.TestCase):
    def test__two_periods_within_filter__returns_two_periods(self):
        filter = PeriodFilter(datetime(2022, 1, 1), datetime(2022, 1, 5))
        task = Task('Test', datetime(2022, 1, 2, 10))
        task.finish(datetime(2022, 1, 2, 11))
        task.periods.append(Period(datetime(2022, 1, 3, 10)))
        task.finish(datetime(2022, 1, 3, 11))

        self.assertTrue(filter.is_valid(task))
        new_task = filter.get_task(task)
        self.assertEqual(len(new_task.periods), 2)

    def test__one_period_before_one_in__returns_one_period(self):
        filter = PeriodFilter(datetime(2022, 1, 3), datetime(2022, 1, 5))
        task = Task('Test', datetime(2022, 1, 2, 10))
        task.finish(datetime(2022, 1, 2, 11))
        task.periods.append(Period(datetime(2022, 1, 3, 10)))
        task.finish(datetime(2022, 1, 3, 11))

        self.assertTrue(filter.is_valid(task))
        new_task = filter.get_task(task)
        self.assertEqual(len(new_task.periods), 1)

    def test__two_periods_within_filter_boundaries__returns_two_periods(self):
        filter = PeriodFilter(datetime(2022, 1, 1), datetime(2022, 1, 5))
        task = Task('Test', datetime(2022, 1, 1))
        task.finish(datetime(2022, 1, 1, 11))
        task.periods.append(Period(datetime(2022, 1, 5)))
        task.finish(datetime(2022, 1, 5, 11))

        self.assertTrue(filter.is_valid(task))
        new_task = filter.get_task(task)
        self.assertEqual(len(new_task.periods), 2)
