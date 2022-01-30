from datetime import date
from datetime import datetime
from clock_framework.datetimeutils import DateTimeUtils
from clock_framework import task

class ClockLogger:
    def __init__(self):
        self.lines = []

    def read_file(self, file):
        try:
            with open(file, 'r') as f:
                self.lines = f.readlines()
            return True
        except Exception:
            return False
        
    def write_file(self, file):
        try:
            with open(file, 'w') as f:
                f.writelines(self.lines)
            return True
        except Exception:
            return False

    def date_exists(self):
        today = date.today()
        for l in self.lines:
            if DateTimeUtils.is_date(l) and DateTimeUtils.get_date(l).date() == today:
                return True

    def add_today(self):
        self.lines.append(date.today().strftime('[%Y-%m-%d]') + '\n')

    def edit_current(self, description):
        if len(self.lines) == 0:
            return
        new_description = self.lines[-1][0:5] + ' ' + description + '\n'
        self.lines[-1] = new_description

    def add(self, at, description):
        if not self.date_exists():
            self.add_today()
        
        new_line = at + ' ' + description + '\n'
        self.lines.append(new_line)

class ClockReader:
    def __init__(self):
        self.lines = []
    
    def read_file(self, filename):
        try:
            file = open(filename, 'r')
            self.lines = [line for line in file]
        except Exception:
            self.lines = []
            print('Could not open file ' + str(filename))

    def parse(self):
        collection = task.TaskCollection()
        current_day = datetime(1900, 1, 1)
        current_task = None
        for line in self.lines:
            if DateTimeUtils.is_date(line):
                current_task and current_task.discard_last()
                current_day = DateTimeUtils.get_date(line)
                current_task = None
                continue

            time = DateTimeUtils.parse_time(current_day, line[0:5])
            current_task and current_task.finish(time)
            current_task = collection.add_task(task.Task(line[6:].replace('\n', ''), time))

        current_task and current_task.finish(datetime.now())
        return collection

