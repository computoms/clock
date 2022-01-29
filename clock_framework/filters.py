from task import Task

class TaskFilterBase:
    def is_valid(self, task):
        return True
    def get_task(self, task):
        return task

class TagFilter(TaskFilterBase):
    def __init__(self, parent_tags):
        self.parent_tags = parent_tags

    def is_valid(self, task):
        return task.is_matching(self.parent_tags)

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
