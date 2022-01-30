import unittest
import datetime
from clock_framework.logger import ClockLogger

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
