from datetime import date
from datetime import datetime
from clock_tracking.datetimeutils import DateTimeUtils
from clock_tracking import task

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
        except Exception as e:
            print('Could not write to file ' + str(file) + ': ' + str(e))
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
        print('Edited: ' + self.lines[-1])

    # Finds position of entry given the 'at' hour (today)
    def find_position(self, at):
        found_today = False
        at_time = DateTimeUtils.parse_time(date.today(), at)
        index = 0
        for line in self.lines:
            if DateTimeUtils.is_date(line) and DateTimeUtils.get_date(line).date() == date.today():
                found_today = True
            elif found_today and not DateTimeUtils.is_date(line):
                current_time = DateTimeUtils.parse_time(date.today(), line[0:5])
                if current_time > at_time:
                    return index
            
            index = index + 1
        return index

    def add(self, at, description):
        if not self.date_exists():
            self.add_today()

        new_line = at + ' ' + description + '\n'
        self.lines.insert(self.find_position(at), new_line)
        print('Added: ' + new_line)

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

