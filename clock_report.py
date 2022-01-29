#!/usr/bin/env python
import sys
import datetime
from clock_framework.taskcollection import TaskCollection
from clock_framework.report import TaskReport
from clock_framework.filters import TagFilter
from clock_framework.filters import DateFilter

# Options
class ReportOptions:
    today = False
    arguments = []

    def parse(self, argv):
        start_index = 1
        if len(argv) > 0 and argv[1] == 'show':
            start_index = 2

        for arg in argv[start_index:]:
            if '--today' in arg:
                self.today = True
            else:
                self.arguments.append(arg)

    def get_filters(self):
        filters = []
        if len(self.arguments) > 0:
            filters.append(TagFilter(self.arguments))
        if self.today:
            filters.append(DateFilter(datetime.datetime.today()))
        return filters

options = ReportOptions()
options.parse(sys.argv)

collection = TaskCollection.from_file('./clock.txt')
for filter in options.get_filters():
    collection = collection.filter(filter)

report = TaskReport(collection)
report.show(len(options.arguments))
report.print_total()