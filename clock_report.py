#!/usr/bin/env python
import sys
import datetime
from clock_framework.taskcollection import TaskCollection
from clock_framework.report import TaskReport
from clock_framework.filters import TagFilter
from clock_framework.filters import DateFilter

# Options
class ReportOptions:
    def __init__(self):
        self.today = False
        self.show_current = False
        self.arguments = []

    def parse(self, argv):
        start_index = 1
        if len(argv) > 1 and argv[1] == 'show':
            start_index = 2
        if len(argv) == 1:
            self.show_current = True

        for arg in argv[start_index:]:
            if '--today' in arg:
                self.today = True
            else:
                self.arguments.append(arg)

    def get_filters(self):
        filters = []
        if len(self.arguments) > 0:
            filters.append(TagFilter(self.arguments))
        if self.today or self.show_current:
            filters.append(DateFilter(datetime.datetime.today()))
        return filters

options = ReportOptions()
options.parse(sys.argv)

collection = TaskCollection.from_file('./clock.txt')
for filter in options.get_filters():
    collection = collection.filter(filter)

if options.show_current and len(collection.tasks) > 1:
    collection.tasks = collection.tasks[-1:]

report = TaskReport(collection)
report.show(len(options.arguments))
report.print_total()