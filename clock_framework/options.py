from datetime import datetime
from datetime import timedelta
import argparse
import sys
from clock_framework.datetimeutils import DateTimeUtils
from clock_framework import filters

class TargetTime:
    def __init__(self, target, is_per_day):
        self.target = target
        self.is_per_day = is_per_day

class ClockArguments:
    def __init__(self):
        self.input_args = sys.argv[1:]
        self.options = None
        self.arguments = []
    
    def parse(self):
        parser = argparse.ArgumentParser(description='Helps managing time tracking')
        parser.add_argument('command', default='add')
        parser.add_argument('-a', '--at', type=str, metavar='HH:MM', default=datetime.today().strftime('%H:%M'), help='<add> Specify a time (format HH:MM) of a new entry')
        parser.add_argument('-c', '--current', action='store_true', help='<add> Modify the description of the current entry')
        parser.add_argument('-f', '--file', type=str, default='./clock.txt', help='Speficy the file to store time entries. Default is ./clock.txt')
        parser.add_argument('-t', '--today', action='store_true', help='<show> Show only entries from today')
        parser.add_argument('-w', '--week', action='store_true', help='<show> Show only entries from the current week')
        parser.add_argument('-s', '--from', type=str, metavar='YYYY-mm-dd', dest='from_', help='<show> Include entries with start date later or equal to given date (format YYYY-mm-dd)')
        parser.add_argument('-e', '--to', type=str, metavar='YYYY-mm-dd', help='<show> Include entries with start date earlier or equal to given date (format YYYY-mm-dd)')
        parser.add_argument('-T', '--target', type=str, metavar='HH:MM', help='<show> Sets expected target time (format HH:MM) and computes the difference with actual times in the reports')
        parser.add_argument('-D', '--target-per-day', type=str, metavar='HH:MM', help='<show> Sets expected target time per day (format HH:MM) and computes the difference with actual times in the reports')
        parser.add_argument('-d', '--details', action='store_true', help='<show> Shows detailed report')

        if len(self.input_args) == 0:
            self.input_args = ['show']

        opt, args = parser.parse_known_args(self.input_args)
        if opt.command not in ('add', 'stop', 'show'):
            args.insert(0, opt.command)
            opt.command = 'add'

        self.options = opt
        self.arguments = args

    def get_target_time(self):
        if self.options.target:
            return TargetTime(DateTimeUtils.parse_duration(self.options.target), False)
        elif self.options.target_per_day:
            return TargetTime(DateTimeUtils.parse_duration(self.options.target_per_day), True)
        return TargetTime(timedelta(0), False)

    def get_filters(self):
        task_filters = []
        if self.options.today:
            task_filters.append(filters.DateFilter(datetime.today()))
        elif self.options.week:
            today = datetime.today()
            monday = today - timedelta(days=today.weekday())
            sunday = monday + timedelta(days=6)
            task_filters.append(filters.PeriodFilter(monday, sunday))
        elif self.options.from_ or self.options.to:
            from_date = datetime(1900, 1, 1)
            to_date = datetime(2100, 1, 1)
            if self.options.from_:
                from_date = datetime.strptime(self.options.from_, '%Y-%m-%d')
            if self.options.to:
                to_date = datetime.strptime(self.options.to, '%Y-%m-%d')
            task_filters.append(filters.PeriodFilter(from_date, to_date))
        if len(self.arguments) > 0:
            task_filters.append(filters.TagFilter(self.arguments))
            task_filters.append(filters.IdFilter(self.arguments))
        return task_filters

   