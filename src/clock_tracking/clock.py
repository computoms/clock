from clock_tracking import logger
from clock_tracking import report
from clock_tracking import options
from clock_tracking import filters
from os.path import expanduser

class ClockCommand():
    def __init__(self, verbs):
        self.verbs = verbs

    def has_verb(self, verb):
        for v in self.verbs:
            if v == verb:
                return True
        return False

    def exec(self):
        pass

class AddCommand(ClockCommand):
    def __init__(self, reader, writer, arguments, file):
        super().__init__(['add'])
        self.reader = reader
        self.writer = writer
        self.args = arguments
        self.file = file

    def exec(self):
        self.writer.read_file(self.file)
        self.writer.add(self.args.options.at, ' '.join(self.args.arguments))
        self.writer.write_file(self.file)
        Clock.report_current(self.file)

class StopCommand(ClockCommand):
    def __init__(self, reader, writer, arguments, file):
        super().__init__(['stop'])
        self.reader = reader
        self.writer = writer
        self.args = arguments
        self.file = file
    
    def exec(self):
        self.writer.read_file(self.file)
        self.writer.add(self.args.options.at, "[Stop]")
        self.writer.write_file(self.file)
        Clock.report_current(self.file)

class EditCommand(ClockCommand):
    def __init__(self, reader, writer, arguments, file):
        super().__init__(['edit'])
        self.reader = reader
        self.writer = writer
        self.args = arguments
        self.file = file

    def exec(self):
        self.writer.read_file(self.file)
        self.writer.edit_current(' '.join(self.args.arguments))
        self.writer.write_file(self.file)
        Clock.report_current(self.file)

class RestartCommand(ClockCommand):
    def __init__(self, reader, writer, arguments, file):
        super().__init__(['restart'])
        self.reader = reader
        self.writer = writer
        self.args = arguments
        self.file = file

    def exec(self):
        self.writer.read_file(self.file)
        desc = self.writer.get_last()
        self.writer.add(self.args.options.at, desc)
        self.writer.write_file(self.file)
        Clock.report_current(self.file)

class ShowCommand(ClockCommand):
    def __init__(self, reader, file, filters, reports):
        super().__init__(['show', 's'])
        self.reader = reader
        self.file = file
        self.filters = filters
        self.reports = reports

    def exec(self):
        self.reader.read_file(self.file)
        collection = self.reader.parse()
        for f in self.filters:
            collection = f.apply_to(collection)
        for r in self.reports:
            r.print_report(collection)


class Clock():
    def __init__(self):
        self.arg = options.ClockArguments()
        self.filters = []
        self.reports = []
        self.file = expanduser('~') + '/clock.txt'
        self._parse_arguments()

    # Parses the arguments from the options.ClockArguments() and 
    # fills in the self.file, self.filters and self.reports
    def _parse_arguments(self):
        self.arg.parse()
        if self.arg.options.file is not None and self.arg.options.file != '':
            self.file = self.arg.options.file
        self.filters = self.arg.get_filters()
        if self.arg.options.command != 'show' and self.arg.options.command != 's':
            return

        if self.arg.options.details:
            self.reports.append(report.DetailsReport())
        elif self.arg.options.timeline and self.arg.options.today:
            self.reports.append(report.DayTimelineReport())
        elif len(self.arg.arguments) > 0 and self.arg.arguments[0] == 'tags':
            self.arg.options.categories = False
            self.reports.append(report.TagsReport())
        elif self.arg.options.categories:
            self.reports.append(report.CategoriesReport(len(self.arg.arguments)))
        if self.arg.options.details or self.arg.options.timeline or self.arg.options.categories:
            self.reports.append(report.TotalTimeReport(self.arg.get_target_time()))

    def get_commands(self):
        return [
            AddCommand(logger.ClockReader(), logger.ClockLogger(), self.arg, self.file), 
            StopCommand(logger.ClockReader(), logger.ClockLogger(), self.arg, self.file), 
            EditCommand(logger.ClockReader(), logger.ClockLogger(), self.arg, self.file), 
            RestartCommand(logger.ClockReader(), logger.ClockLogger(), self.arg, self.file),
            ShowCommand(logger.ClockReader(), self.file, self.filters, self.reports)]

    def exec(self):
        command = self.arg.options.command

        # Dispatch command
        for c in self.get_commands():
            if c.has_verb(command):
                c.exec()

    # Shows current issue report
    @staticmethod
    def report_current(file):
        ShowCommand(logger.ClockReader(), file, [filters.LastFilter(1)], [report.DetailsReport()]).exec()

    # Single static method to run script according to command line arguments
    @staticmethod
    def run():
        clock = Clock()
        clock.exec()
