import unittest
import datetime

from clock_framework.options import ClockOptions
from clock_framework.options import Commands

class TestOptionsExtractCommand(unittest.TestCase):
    def test__command_show__extracts_command_show(self):
        opt = ClockOptions()
        opt.extract_command(['clock', 'show'])

        self.assertEqual(opt.command, Commands.show)

    def test__command_add__extracts_command_add(self):
        opt = ClockOptions()
        opt.extract_command(['clock', 'add'])

        self.assertEqual(opt.command, Commands.add)

    def test__command_stop__extracts_command_stop(self):
        opt = ClockOptions()
        opt.extract_command(['clock', 'stop'])

        self.assertEqual(opt.command, Commands.stop)

    def test__no_command__returns_arg_list_without_first(self):
        opt = ClockOptions()
        args = opt.extract_command(['clock', 'this', 'is', 'test'])

        self.assertEqual(len(args), 3)
        self.assertEqual(args[0], 'this')

class TestOptionsParse(unittest.TestCase):
    def test__empty__returns_default_options(self):
        opt = ClockOptions()
        opt.parse(['clock'])

        for s in opt.switch_list:
            self.assertFalse(s.is_active)
        self.assertEquals(opt.file.value, './clock.txt')

    def test__at__returns_at(self):
        opt = ClockOptions()
        opt.parse(['clock', '--at', '08:10'])

        self.assertTrue(opt.at.is_active)
        self.assertEqual(opt.at.value, '08:10')

    def test__file__returns_file(self):
        opt = ClockOptions()
        opt.parse(['clock', '--file', './clock-test.txt'])

        self.assertTrue(opt.file.is_active)
        self.assertEqual(opt.file.value, './clock-test.txt')

    def test__from__returns_from(self):
        opt = ClockOptions()
        opt.parse(['clock', '--from', '2022-01-02'])

        self.assertTrue(opt.from_filter.is_active)
        self.assertEqual(opt.from_filter.value, '2022-01-02')

    def test__to__returns_to(self):
        opt = ClockOptions()
        opt.parse(['clock', '--to', '2022-01-02'])

        self.assertTrue(opt.to_filter.is_active)
        self.assertEqual(opt.to_filter.value, '2022-01-02')

    def test__today_long__enables_today(self):
        opt = ClockOptions()
        opt.parse(['clock', '--today'])

        self.assertTrue(opt.today.is_active)

    def test__today_short__enables_today(self):
        opt = ClockOptions()
        opt.parse(['clock', '-t'])

        self.assertTrue(opt.today.is_active)

    def test__week_long__enables_week(self):
        opt = ClockOptions()
        opt.parse(['clock', '--week'])

        self.assertTrue(opt.this_week.is_active)

    def test__week_short__enables_week(self):
        opt = ClockOptions()
        opt.parse(['clock', '-w'])

        self.assertTrue(opt.this_week.is_active)