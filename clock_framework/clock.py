from clock_framework import logger
from clock_framework import report
from clock_framework import options
from os.path import expanduser

class Clock():
    def __init__(self):
        self.reader = logger.ClockReader()
        self.writer = logger.ClockLogger()
        self.arg = options.ClockArguments()

        self.filters = []
        self.reports = []
        self.file = expanduser('~') + '/clock.txt'

    # Parses the arguments from the options.ClockArguments() and 
    # fills in the self.file, self.filters and self.reports
    def parse_arguments(self):
        self.arg.parse()
        if self.arg.options.file is not None and self.arg.options.file != '':
            self.file = self.arg.options.file
        self.filters = self.arg.get_filters()
        if self.arg.options.command != 'show':
            return

        if self.arg.options.details:
            self.reports.append(report.ChronologicalReport())
        elif self.arg.options.categories:
            self.reports.append(report.CategoriesReport(len(self.arg.arguments)))
        self.reports.append(report.TotalTimeReport(self.arg.get_target_time()))

    # Filters issues according to self.filters and shows reports in self.reports
    def show(self):
        self.reader.read_file(self.file)
        collection = self.reader.parse()
        for f in self.filters:
            collection = f.apply_to(collection)
        for r in self.reports:
            r.print_report(collection)

    # Shows current issue report
    def report_current(self):
        self.reader.read_file(self.file)
        collection = self.reader.parse()
        report.CurrentIssueReport().print_report(collection)

    # Add new entry at given time (at) with given description (description)
    def add(self, at, description):
        self.writer.read_file(self.file)
        self.writer.add(at, description)
        self.writer.write_file(self.file)

    # Edits current entry by replacing its description by given description
    def edit(self, description):
        self.writer.read_file(self.file)
        self.writer.edit_current(description)
        self.writer.write_file(self.file)

    # Single static method to run script according to command line arguments
    @staticmethod
    def run():
        clock = Clock()
        clock.parse_arguments()
        options = clock.arg.options

        if options.command == 'show':
            clock.show()
        elif options.command == 'add':
            clock.add(options.at, ' '.join(clock.arg.arguments))
        elif options.command == 'edit':
            clock.edit(' '.join(clock.arg.arguments))
        elif options.command == 'stop':
            clock.add(options.at, '[Stop]')

        if options.command in ('add', 'edit', 'stop'):
            clock.report_current()
