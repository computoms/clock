import unittest
import datetime
from clock_tracking.task import Task, Period, TaskCollection

class TestTaskParse(unittest.TestCase):
    def test__single_description__parses_correctly(self):
        t = Task('this is a test', datetime.datetime.now())
        self.assertTrue(t.description == 'this is a test')
        self.assertTrue(len(t.tags) == 0)
        self.assertTrue(len(t.periods) == 1)

    def test__description_with_one_tag__parse_one_tag(self):
        t = Task("this is a description with one +tag", datetime.datetime.now())
        self.assertTrue(len(t.tags) == 1)
        self.assertTrue(t.tags[0] == '+tag')

    def test__description_with_two_tags__parses_two_tags(self):
        t = Task("this is a description with two +tag +tag2", datetime.datetime.now())
        self.assertTrue(len(t.tags) == 2)
        self.assertTrue(t.tags[1] == '+tag2')

    def test__with_id__parses_id(self):
        t = Task("test with id .4537", datetime.datetime.now())
        self.assertTrue(len(t.ids) == 1)
        self.assertTrue(t.ids[0] == '.4537')

    def test__with_id__adds_jira_tag(self):
        t = Task("test with id .4537", datetime.datetime.now())
        self.assertTrue(len(t.tags) == 1)
        self.assertTrue(t.tags[0] == '+jira')

    def test__with_id__removes_id_from_description(self):
        t = Task("test with id .4537", datetime.datetime.now())
        self.assertTrue(t.description == 'test with id')

    def test__with_new_line__removes_new_line(self):
        t = Task("test with new line\n", datetime.datetime.now())
        self.assertTrue(t.description == 'test with new line')

    def test__with_cariage_return__removes_new_line(self):
        t = Task("test with new line\r", datetime.datetime.now())
        self.assertTrue(t.description == 'test with new line')

class TestTaskIsStop(unittest.TestCase):
    def test__when_stop__returns_true(self):
        t = Task('[Stop]', datetime.datetime.now())
        self.assertTrue(t.is_stop())

    def test__with_spaces__returns_true(self):
        t = Task(' [Stop]  ', datetime.datetime.now())
        self.assertTrue(t.is_stop())

    def test__not_stop__returns_false(self):
        t = Task(' [Stop', datetime.datetime.now())
        self.assertTrue(not t.is_stop())

class TestTaskFinish(unittest.TestCase):
    def test__no_periods__does_not_throw(self):
        t = Task('test', datetime.datetime.now())
        t.periods = []
        t.finish(datetime.datetime.now())

    def test__one_task__finishes_task(self):
        t = Task('test', datetime.datetime.now())
        t.finish(datetime.datetime.now())
        self.assertTrue(len(t.periods) == 1)
        self.assertTrue(t.periods[0].end.year != 1900)

class TestTaskDiscardLast(unittest.TestCase):
    def test__no_periods__does_not_throw(self):
        t = Task('test', datetime.datetime.now())
        t.periods = []
        t.discard_last()

    def test__one_period__clears_periods(self):
        t = Task('test', datetime.datetime.now())
        t.discard_last()
        self.assertTrue(len(t.periods) == 0)

class TestTaskIsMatching(unittest.TestCase):
    def test__no_tag__returns_true(self):
        t = Task('test', datetime.datetime.now())
        self.assertTrue(t.is_matching([]))

    def test__one_tag__returns_true(self):
        t = Task('test +cat', datetime.datetime.now())
        self.assertTrue(t.is_matching(['+cat']))

    def test__one_tag_different__returns_false(self):
        t = Task('test +cat', datetime.datetime.now())
        self.assertTrue(not t.is_matching(['+test']))

    def test__two_tags__returns_true(self):
        t = Task('test +cat1 +cat2', datetime.datetime.now())
        self.assertTrue(t.is_matching(['+cat1', '+cat2']))

    def test__two_tags_wrong_order__returns_false(self):
        t = Task('test +cat2 +cat1', datetime.datetime.now())
        self.assertTrue(not t.is_matching(['+cat1', '+cat2']))

    def test__one_tag_testing_two__returns_false(self):
        t = Task('test +cat', datetime.datetime.now())
        self.assertTrue(not t.is_matching(['+cat', '+cat2']))

class TestTaskDurationTotal(unittest.TestCase):
    def test__empty__returns_zero(self):
        t = Task('test', datetime.datetime.now())
        t.periods = []
        self.assertTrue(t.duration_total().seconds == 0)

    def test__one__returns_one(self):
        t = Task('test', datetime.datetime(2022,1,1,10,0,0))
        t.finish(datetime.datetime(2022,1,1,11,0,0))
        self.assertTrue(t.duration_total().seconds == 3600)

    def test__two__returns_sum(self):
        t = Task('test', datetime.datetime(2022, 1, 1, 10, 0, 0))
        t.finish(datetime.datetime(2022, 1, 1, 10, 30, 0))
        p = Period(datetime.datetime(2022,1,1,12,0,0))
        p.end = datetime.datetime(2022, 1, 1, 12, 30, 0)
        t.periods.append(p)
        self.assertTrue(t.duration_total().seconds == 3600)

class TestTaskEquals(unittest.TestCase):
    def test__different_description__returns_false(self):
        t = Task('test1', datetime.datetime.now())
        t2 = Task('test2', datetime.datetime.now())
        self.assertTrue(not t.equals(t2))

    def test__different_tags__returns_false(self):
        t = Task('test +tag', datetime.datetime.now())
        t2 = Task('test', datetime.datetime.now())
        self.assertTrue(not t.equals(t2))

    def test__are_equal__returns_true(self):
        t = Task('test +tag', datetime.datetime.now())
        t2 = Task('test +tag', datetime.datetime.now())
        self.assertTrue(t.equals(t2))

class TestTaskCopyEmpty(unittest.TestCase):
    def test__non_empty_task__returns_empty_task(self):
        t = Task('test', datetime.datetime.now())
        self.assertTrue(len(t.periods) != 0)
        t2 = t.copy_empty()
        self.assertTrue(len(t2.periods) == 0)

class TestTaskCollectionExists(unittest.TestCase):
    def test__existing_task__return_true(self):
        c = TaskCollection()
        task = Task('test', datetime.datetime.now())
        c.tasks.append(task)
        self.assertTrue(c.exists(task))

    def test__non_existing_task__returns_false(self):
        c = TaskCollection()
        task = Task('test', datetime.datetime.now())
        self.assertTrue(not c.exists(task))

class TestTaskCollectionGetTask(unittest.TestCase):
    def test__non_existing_task__returns_none(self):
        c = TaskCollection()
        task = Task('test', datetime.datetime.now())
        self.assertTrue(c.get_task(task) is None)

    def test__existing_task__returns_task(self):
        c = TaskCollection()
        task = Task('test', datetime.datetime.now())
        c.tasks.append(task)
        self.assertTrue(c.get_task(task).equals(task))
    
class TestTaskCollectionAddTask(unittest.TestCase):
    def test__stop__does_not_add_task(self):
        c = TaskCollection()
        task = Task('[Stop]', datetime.datetime.now())
        c.add_task(task)
        self.assertTrue(len(c.tasks) == 0)

    def test__non_existing_task__adds_task(self):
        c = TaskCollection()
        task = Task('test', datetime.datetime.now())
        c.add_task(task)
        self.assertTrue(len(c.tasks) == 1)

    def test__existing_task__adds_periods(self):
        c = TaskCollection()
        task = Task('test', datetime.datetime(2022, 1, 1, 9))
        task.finish(datetime.datetime(2022, 1, 1, 10))
        c.add_task(task)
        task2 = Task('test', datetime.datetime(2022, 1, 1, 11))
        c.add_task(task2)
        self.assertTrue(len(c.tasks) == 1)
        self.assertTrue(len(c.tasks[0].periods) == 2)

    def test__existing_task__returns_existing_task(self):
        c = TaskCollection()
        task = Task('test', datetime.datetime(2022, 1, 1, 9))
        task.finish(datetime.datetime(2022, 1, 1, 10))
        c.add_task(task)
        task2 = Task('test', datetime.datetime(2022, 1, 1, 11))
        result = c.add_task(task2)
        self.assertTrue(result == task)

