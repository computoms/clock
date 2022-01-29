import datetime
from datetimeutils import DateTimeUtils
from task import Task

class TaskCollection:
    def __init__(self):
        self.tasks = []

    def exists(self, task):
        for t in self.tasks:
            if t.equals(task):
                return True
        return False

    def get_task(self, task):
        for t in self.tasks:
            if t.equals(task):
                return t
        return None

    def add_task(self, task):
        if task.is_stop(): # Do not add [Stop] tasks
            return task
        # If task already exists, add its periods
        if self.exists(task): 
            t = self.get_task(task)
            for p in task.periods:
                t.periods.append(p)
            return t

        self.tasks.append(task)
        return task

    @staticmethod
    def from_file(filename):
        file = open(filename, 'r')
        lines = [line for line in file]
        return TaskCollection.from_lines(lines)

    @staticmethod
    def from_lines(lines):
        collection = TaskCollection()
        current_day = datetime.datetime(1900, 1, 1)
        current_task = None
        for line in lines:
            if DateTimeUtils.is_date(line):
                current_task and current_task.discard_last()
                current_day = DateTimeUtils.get_date(line)
                current_task = None
                continue

            time = DateTimeUtils.parse_time(current_day, line[0:5])
            current_task and current_task.finish(time)
            current_task = collection.add_task(Task(line[6:].replace('\n', ''), time))

        current_task and current_task.finish(datetime.datetime.now())
        return collection


    def filter(self, filter):
        c = TaskCollection()
        c.tasks = [filter.get_task(task) for task in self.tasks if filter.is_valid(task)]
        return c
