from ..taskcollection import TaskCollection
from ..task import Task
import datetime

from clock_framework import taskcollection

def exists_existingtask_returntrue():
    c = TaskCollection()
    task = Task('test', datetime.datetime.now())
    c.tasks.append(task)
    assert(c.exists(task))

def exists_nonexistingtask_returnsfalse():
    c = TaskCollection()
    task = Task('test', datetime.datetime.now())
    assert(not c.exists(task))

def gettask_nonexistingtask_returnsnone():
    c = TaskCollection()
    task = Task('test', datetime.datetime.now())
    assert(c.get_task(task) is None)

def gettask_existingtask_returnstask():
    c = TaskCollection()
    task = Task('test', datetime.datetime.now())
    c.tasks.append(task)
    assert(c.get_task(task).equals(task))

def addtask_stop_doesnotaddtask():
    c = TaskCollection()
    task = Task('[Stop]', datetime.datetime.now())
    c.add_task(task)
    assert(len(c.tasks) == 0)

def addtask_nonexistingtask_addstask():
    c = TaskCollection()
    task = Task('test', datetime.datetime.now())
    c.add_task(task)
    assert(len(c.tasks) == 1)

def addtask_existingtask_addsperiods():
    c = TaskCollection()
    task = Task('test', datetime.datetime(2022, 1, 1, 9))
    task.finish(datetime.datetime(2022, 1, 1, 10))
    c.add_task(task)
    task2 = Task('test', datetime.datetime(2022, 1, 1, 11))
    c.add_task(task2)
    assert(len(c.tasks) == 1)
    assert(len(c.tasks[0].periods) == 2)

def addtask_existingtask_returnsexistingtask():
    c = TaskCollection()
    task = Task('test', datetime.datetime(2022, 1, 1, 9))
    task.finish(datetime.datetime(2022, 1, 1, 10))
    c.add_task(task)
    task2 = Task('test', datetime.datetime(2022, 1, 1, 11))
    result = c.add_task(task2)
    assert(result == task)

def parse_dateonly_returnsempty():
    c = TaskCollection.from_lines(['[2022-01-01]'])
    assert(len(c.tasks) == 0)

def parse_dateandtask_returnsonetask():
    c = TaskCollection.from_lines(['[2022-01-01]', '09:00 task1'])
    assert(len(c.tasks) == 1)

def parse_taskwithoutdate_returnstaskwithdefaultdate():
    c = TaskCollection.from_lines(['09:00 task1'])
    assert(len(c.tasks) == 1)
    assert(len(c.tasks[0].periods) == 1)
    assert(c.tasks[0].periods[0].start.date().year == 1900)

def parse_missingstop_removeslasttaskofday():
    c = TaskCollection.from_lines(['[2022-01-01]', '09:00 task without stop', '[2022-01-02]'])
    assert(len(c.tasks) == 1)
    assert(len(c.tasks[0].periods) == 0)

def parse_taskwithstop_finsihestask():
    c = TaskCollection.from_lines(['[2022-01-01]', '09:00 task with stop', '09:10 [Stop]'])
    assert(len(c.tasks) == 1)
    assert(len(c.tasks[0].periods) == 1)
    assert(c.tasks[0].duration_total().seconds == 600)

def parse_sametasks_addspeiods():
    c = TaskCollection.from_lines(['[2022-01-01]', '09:00 task', '10:00 task2', '11:00 task', '12:00 [Stop]'])
    assert(len(c.tasks) == 2)
    assert(len(c.tasks[0].periods) == 2)
    assert(c.tasks[0].duration_total().seconds == 7200)

def parse_emptyday_doesnotaddtask():
    c = TaskCollection.from_lines(['[2022-01-01]', '09:00 task', '10:00 [Stop]', '[2022-01-02]', '[2022-01-03]', '09:00 task1'])
    assert(len(c.tasks) == 2)

def run():
    exists_existingtask_returntrue()
    exists_nonexistingtask_returnsfalse()

    gettask_nonexistingtask_returnsnone()
    gettask_existingtask_returnstask()

    addtask_stop_doesnotaddtask()
    addtask_nonexistingtask_addstask()
    addtask_existingtask_addsperiods()
    addtask_existingtask_returnsexistingtask()

    parse_dateonly_returnsempty()
    parse_dateandtask_returnsonetask()
    parse_taskwithoutdate_returnstaskwithdefaultdate()
    parse_missingstop_removeslasttaskofday()
    parse_taskwithstop_finsihestask()
    parse_sametasks_addspeiods()
    parse_emptyday_doesnotaddtask()