import unittest
import datetime
from clock_framework.taskcollection import TaskCollection
from clock_framework.task import Task

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

class TestTaskCollectionParse(unittest.TestCase):
    def test__date_only__returns_empty(self):
        c = TaskCollection.from_lines(['[2022-01-01]'])
        self.assertTrue(len(c.tasks) == 0)

    def test__date_and_task__returns_one_task(self):
        c = TaskCollection.from_lines(['[2022-01-01]', '09:00 task1'])
        self.assertTrue(len(c.tasks) == 1)

    def test__task_without_date__returns_task_with_default_date(self):
        c = TaskCollection.from_lines(['09:00 task1'])
        self.assertTrue(len(c.tasks) == 1)
        self.assertTrue(len(c.tasks[0].periods) == 1)
        self.assertTrue(c.tasks[0].periods[0].start.date().year == 1900)

    def test__missing_stop__removes_last_task_of_day(self):
        c = TaskCollection.from_lines(['[2022-01-01]', '09:00 task without stop', '[2022-01-02]'])
        self.assertTrue(len(c.tasks) == 1)
        self.assertTrue(len(c.tasks[0].periods) == 0)

    def test__task_with_stop__finishes_task(self):
        c = TaskCollection.from_lines(['[2022-01-01]', '09:00 task with stop', '09:10 [Stop]'])
        self.assertTrue(len(c.tasks) == 1)
        self.assertTrue(len(c.tasks[0].periods) == 1)
        self.assertTrue(c.tasks[0].duration_total().seconds == 600)

    def test__same_tasks__adds_periods(self):
        c = TaskCollection.from_lines(['[2022-01-01]', '09:00 task', '10:00 task2', '11:00 task', '12:00 [Stop]'])
        self.assertTrue(len(c.tasks) == 2)
        self.assertTrue(len(c.tasks[0].periods) == 2)
        self.assertTrue(c.tasks[0].duration_total().seconds == 7200)

    def test__empty_day__does_not_add_task(self):
        c = TaskCollection.from_lines(['[2022-01-01]', '09:00 task', '10:00 [Stop]', '[2022-01-02]', '[2022-01-03]', '09:00 task1'])
        self.assertTrue(len(c.tasks) == 2)
