from clock_tracking.task import Task
from clock_tracking.task import TaskCollection

class TaskFilterBase:
    def is_valid(self, task):
        return True
    def get_task(self, task):
        return task
    def apply_to(self, collection):
        c = TaskCollection()
        c.tasks = [t for t in collection.tasks if self.is_valid(t)]
        return c

class TagFilter(TaskFilterBase):
    def __init__(self, args):
        self.parent_tags = []
        for arg in args:
            if '+' in arg:
                self.parent_tags.append(arg)

    def is_valid(self, task):
        return task.is_matching(self.parent_tags)

class IdFilter(TaskFilterBase):
    def __init__(self, args):
        self.ids = []
        for arg in args:
            if '.' in arg:
                self.ids.append(arg)
    
    def is_valid(self, task):
        if len(self.ids) == 0:
            return True

        for id in self.ids:
            if id in task.ids:
                return True
        return False

class DateFilter(TaskFilterBase):
    def __init__(self, date):
        self.date = date

    def is_valid(self, task):
        if len(task.periods) == 0:
            return False
        for p in task.periods:
            if p.start.date() == self.date.date():
                return True
        return False

    def get_task(self, task):
        t = task.copy_empty()
        for p in task.periods:
            if p.start.date() == self.date.date():
                t.periods.append(p)

        return t

    def apply_to(self, collection):
        c = TaskCollection()
        c.tasks = [self.get_task(t) for t in collection.tasks if self.is_valid(t)]
        return c

class PeriodFilter(TaskFilterBase):
    def __init__(self, date_start, date_end):
        self.date_start = date_start.date()
        self.date_end = date_end.date()

    def is_valid(self, task):
        if len(task.periods) == 0:
            return False
        for p in task.periods:
            if p.start.date() >= self.date_start and p.start.date() <= self.date_end: # TODO we should probably also check the p.end.date() but it's supposed to be the same date in current architecture
                return True
        return False
    
    def get_task(self, task):
        t = task.copy_empty()
        for p in task.periods:
            if p.start.date() >= self.date_start and p.start.date() <= self.date_end:
                t.periods.append(p)

        return t

    def apply_to(self, collection):
        c = TaskCollection()
        c.tasks = [self.get_task(t) for t in collection.tasks if self.is_valid(t)]
        return c

class LastFilter(TaskFilterBase):
    def __init__(self, count):
        self.count = count

    def apply_to(self, collection):
        c = TaskCollection()
        periods = []
        for task in collection.tasks:
            for p in task.periods:
                periods.append([p, task])

        ordered_periods = sorted(periods, key=lambda t: t[0].start, reverse=True)
        for i in range(self.count):
            if i < len(ordered_periods):
                t = ordered_periods[i][1].copy_empty()
                t.periods.append(ordered_periods[i][0])
                c.tasks.append(t)

        return c

