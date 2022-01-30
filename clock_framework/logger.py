from datetime import date
from clock_framework.datetimeutils import DateTimeUtils
import datetimeutils

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
