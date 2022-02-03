import unittest
import datetime
from clock_tracking.logger import ClockLogger, ClockReader

class TestClockLoggerDateExists(unittest.TestCase):
    def test__empty__returns_false(self):
        logger = ClockLogger()
        self.assertFalse(logger.date_exists())

    def test__single_not_today__returns_false(self):
        logger = ClockLogger()
        logger.lines = ['[2022-01-01]\n']
        self.assertFalse(logger.date_exists())

    def test__single_today__returns_true(self):
        logger = ClockLogger()
        logger.lines = ['[' + datetime.datetime.today().strftime('%Y-%m-%d')+ ']\n']
        self.assertTrue(logger.date_exists())

    def test_dual_with_today__returns_true(self):
        logger = ClockLogger()
        logger.lines = ['[2022-01-01]\n', '[' + datetime.datetime.today().strftime('%Y-%m-%d')+ ']\n']
        self.assertTrue(logger.date_exists())

class TestClockLoggerEditCurrent(unittest.TestCase):
    def test__empty__does_nothing(self):
        logger = ClockLogger()
        logger.edit_current('Test')
        self.assertTrue(len(logger.lines) == 0)

    def test__one_line__edits_line(self):
        logger = ClockLogger()
        logger.lines = ['09:00 Test\n']
        logger.edit_current('Test2')
        self.assertEqual(len(logger.lines), 1)
        self.assertEqual(logger.lines[0], '09:00 Test2\n')

class TestClockLoggerAdd(unittest.TestCase):
    def test__with_today__adds_one_line(self):
        logger = ClockLogger()
        logger.lines = ['[' + datetime.datetime.today().strftime('%Y-%m-%d') + ']\n']
        logger.add('09:00', 'Test')
        self.assertTrue(len(logger.lines) == 2)
        self.assertEqual(logger.lines[1], '09:00 Test\n')
    
    def test__empty__adds_today_with_line(self):
        logger = ClockLogger()
        logger.add('09:00', 'Test')
        self.assertTrue(len(logger.lines) == 2)
        self.assertEqual(logger.lines[1], '09:00 Test\n')

class TestClockReaderParse(unittest.TestCase):
    def test__date_only__returns_empty(self):
        reader = ClockReader()
        reader.lines = ['[2022-01-01]']
        c = reader.parse()
        self.assertTrue(len(c.tasks) == 0)

    def test__date_and_task__returns_one_task(self):
        reader = ClockReader()
        reader.lines = ['[2022-01-01]', '09:00 task1']
        c = reader.parse()
        self.assertTrue(len(c.tasks) == 1)

    def test__task_without_date__returns_task_with_default_date(self):
        reader = ClockReader()
        reader.lines = ['09:00 task1']
        c = reader.parse()
        self.assertTrue(len(c.tasks) == 1)
        self.assertTrue(len(c.tasks[0].periods) == 1)
        self.assertTrue(c.tasks[0].periods[0].start.date().year == 1900)

    def test__missing_stop__removes_last_task_of_day(self):
        reader = ClockReader()
        reader.lines = ['[2022-01-01]', '09:00 task without stop', '[2022-01-02]']
        c = reader.parse()
        self.assertTrue(len(c.tasks) == 1)
        self.assertTrue(len(c.tasks[0].periods) == 0)

    def test__task_with_stop__finishes_task(self):
        reader = ClockReader()
        reader.lines = ['[2022-01-01]', '09:00 task with stop', '09:10 [Stop]']
        c = reader.parse()
        self.assertTrue(len(c.tasks) == 1)
        self.assertTrue(len(c.tasks[0].periods) == 1)
        self.assertTrue(c.tasks[0].duration_total().seconds == 600)

    def test__same_tasks__adds_periods(self):
        reader = ClockReader()
        reader.lines = ['[2022-01-01]', '09:00 task', '10:00 task2', '11:00 task', '12:00 [Stop]']
        c = reader.parse()
        self.assertTrue(len(c.tasks) == 2)
        self.assertTrue(len(c.tasks[0].periods) == 2)
        self.assertTrue(c.tasks[0].duration_total().seconds == 7200)

    def test__empty_day__does_not_add_task(self):
        reader = ClockReader()
        reader.lines = ['[2022-01-01]', '09:00 task', '10:00 [Stop]', '[2022-01-02]', '[2022-01-03]', '09:00 task1']
        c = reader.parse()
        self.assertTrue(len(c.tasks) == 2)
