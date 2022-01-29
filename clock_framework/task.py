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
            if word[0] == '+':
                self.tags.append(word.strip())
            elif word[0] == '.':
                self.ids.append(word.strip())
            else:
                desc += word + ' '
        self.description = desc.strip()
        if len(self.ids) > 0:
            new_tags = ['+jira']
            for tag in self.tags:
                new_tags.append(tag)
            self.tags = new_tags

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
        t.periods = []
        return t
