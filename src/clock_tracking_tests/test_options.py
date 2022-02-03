import unittest
import datetime
from clock_tracking import datetimeutils, options

class TestClockArgumentsGetTargetTime(unittest.TestCase):
    def test__global_target__returns_global_target(self):
        args = options.ClockArguments()
        args.input_args = ['show', '--target', '150:00']
        args.parse()
        target_time = args.get_target_time()

        self.assertFalse(target_time.is_per_day)
        self.assertEqual(target_time.target, datetime.timedelta(0, 150*3600))

    def test__taget_per_day__returns_target_per_day(self):
        args = options.ClockArguments()
        args.input_args = ['show', '--target-per-day', '8:24']
        args.parse()
        target_time = args.get_target_time()

        self.assertTrue(target_time.is_per_day)
        self.assertEqual(target_time.target, datetime.timedelta(0, 8*3600 + 24*60))

class TestClockArgumentsGetFilters(unittest.TestCase):
    def test__today_and_week__returns_today(self):
        args = options.ClockArguments()
        args.input_args = ['show', '--today', '--week']
        args.parse()
        filters = args.get_filters()

        self.assertTrue(len(filters) == 1)
        self.assertEqual(filters[0].date.date(), datetime.datetime.today().date())

    def test__week_and_from__returns_week(self):
        args = options.ClockArguments()
        args.input_args = ['show', '--week', '--from', '2022-01-01']
        args.parse()
        filters = args.get_filters()

        start_week = datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().weekday())
        end_week = start_week + datetime.timedelta(days=6)

        self.assertTrue(len(filters) == 1)
        self.assertEqual(filters[0].date_start, start_week.date())
        self.assertEqual(filters[0].date_end, end_week.date())

class TestClockArgumentsParse(unittest.TestCase):
    def test__without_command__adds_default_add(self):
        args = options.ClockArguments()
        args.input_args = ['This', 'is', 'a', 'test']
        args.parse()
        
        self.assertEqual(args.options.command, 'add')

    def test__without_argument__adds_show_command(self):
        args = options.ClockArguments()
        args.input_args = []
        args.parse()
        
        self.assertEqual(args.options.command, 'show')