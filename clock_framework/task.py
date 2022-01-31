import datetime

class Period:
    def __init__(self, start):
        self.start = start
        self.end = datetime.datetime(1900,1,1)

class Task:
    def __init__(self, description, start):
        self.description = ''
        self.periods = []
        self.tags = []
        self.ids = []
        self.parse(description)
        self.periods.append(Period(start))
    
    def parse(self, description):
        description = description.replace('\r', '').replace('\n', '')
        words = description.split(' ')
        desc = ''
        for word in words:
            if len(word) == 0:
                continue
            if word[0] == '+' and len(word) > 1:
                self.tags.append(word.strip())
            elif word[0] == '.' and len(word) > 1:
                self.ids.append(word.strip())
            else:
                desc += word + ' '
        self.description = desc.strip()
        if len(self.ids) > 0:
            self.tags.insert(0, '+jira')

    def is_stop(self):
        return '[Stop]' in self.description

    def finish(self, end):
        if len(self.periods) > 0:
            self.periods[-1].end = end

    def discard_last(self):
        if len(self.periods) == 0:
            return
        self.periods.pop()

    def is_matching(self, parent_tags):
        for i in range(0, len(parent_tags)):
            if len(self.tags) <= i:
                return False
            if self.tags[i] != parent_tags[i]:
                return False
        return True

    def duration_total(self):
        total_time = datetime.timedelta()
        for period in self.periods:
            total_time += period.end - period.start
        return total_time

    def equals(self, task):
        if self.description != task.description:
            return False
        for tag in self.tags:
            if not tag in task.tags:
                return False
        return True
    
    def copy_empty(self):
        t = Task(self.description, datetime.datetime.now())
        t.tags = self.tags
        t.ids = self.ids
        t.periods = []
        return t

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

    def filter(self, filter):
        c = TaskCollection()
        c.tasks = [filter.get_task(task) for task in self.tasks if filter.is_valid(task)]
        return c