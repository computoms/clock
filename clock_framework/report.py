import datetime
from xmlrpc.client import DateTime
from clock_framework.datetimeutils import DateTimeUtils
from clock_framework.colors import TerminalColors

class PrintHelpers:
    graph_width = 40
    color_index = -1

    @staticmethod
    def get_graph(time, totaltime):
        char_width = DateTimeUtils.get_seconds(time) * PrintHelpers.graph_width / DateTimeUtils.get_seconds(totaltime)
        result = [u'\u2588' for i in range(int(char_width))]
        result.extend([' ' for i in range(int(char_width), PrintHelpers.graph_width)])
        return ''.join(result)

    # TODO replace with match-case (python3)
    @staticmethod
    def get_color():
        PrintHelpers.color_index = PrintHelpers.color_index + 1
        if PrintHelpers.color_index > 2:
            PrintHelpers.color_index = 0

        if PrintHelpers.color_index == 0:
            return TerminalColors.BLUE
        elif PrintHelpers.color_index == 1:
            return TerminalColors.CYAN
        return TerminalColors.GREEN

    @staticmethod
    def max_width(string, width):
        if len(string) < width:
            return string.ljust(width)

        return (string[0:(width-3)] + '...').ljust(width)

    @staticmethod
    def colorize(string, color):
        if not TerminalColors.enabled:
            return string
        return color + string + TerminalColors.END


class TaskReportBase(object):
    def __init__(self):
        pass

    def print_report(self, collection):
        print('')

# Print details of all entries in collection
class DetailsReport(TaskReportBase):
    def __init__(self):
        super(DetailsReport, self).__init__()

    def print_report(self, collection):
        tasks = sorted(collection.tasks, key=lambda t: t.periods[-1].start)
        for task in tasks:
            desc = task.description + ' '
            for tag in task.tags:
                desc += tag + ' '
            desc = desc.ljust(30)
            print(desc)
            print(DateTimeUtils.show_timedelta(task.duration_total()))
            for p in task.periods:
                print('                               . ' \
                    + DateTimeUtils.show_timedelta(p.end - p.start) + ' : ' + DateTimeUtils.show_date(p.start) + ' ' + DateTimeUtils.show_time(p.start) + ' --> ' \
                    + DateTimeUtils.show_date(p.end) + ' ' + DateTimeUtils.show_time(p.end))

# Prints periods in chronological order
class ChronologicalReport(TaskReportBase):
    def __init__(self):
        super(ChronologicalReport, self).__init__()

    def print_report(self, collection):
        periods = []
        for task in collection.tasks:
            for p in task.periods:
                periods.append([p, task])

        periods = sorted(periods, key=lambda t: t[0].start)

        print(str('Duration').ljust(10) + 'Date'.ljust(12) + 'Start'.ljust(6) + 'Stop'.ljust(6) + 'Tags'.ljust(20) + 'IDs'.ljust(10) + 'Name'.ljust(40))
        for kv in periods:
            p = kv[0]
            print(PrintHelpers.colorize(DateTimeUtils.show_timedelta(p.end - p.start).ljust(10), TerminalColors.GREEN) \
                + DateTimeUtils.show_date(p.start).ljust(12) \
                + DateTimeUtils.show_time(p.start).ljust(6) \
                + DateTimeUtils.show_time(p.end).ljust(6) \
                + PrintHelpers.colorize(PrintHelpers.max_width(','.join(kv[1].tags), 20), TerminalColors.BLUE) \
                + PrintHelpers.colorize(PrintHelpers.max_width(','.join(kv[1].ids), 10), TerminalColors.BOLD) \
                + PrintHelpers.max_width(kv[1].description, 40))

# Prints current issue
class CurrentIssueReport(TaskReportBase):
    def __init__(self):
        super(CurrentIssueReport, self).__init__()

    def print_report(self, collection):
        latest_period = None
        latest_task = None
        for task in collection.tasks:
            for p in task.periods:
                if latest_period is None or latest_period.start < p.start:
                    latest_period = p
                    latest_task = task

        print(str('Duration').ljust(10) + 'Date'.ljust(12) + 'Start'.ljust(6) + 'Stop'.ljust(6) + 'Tags'.ljust(20) + 'IDs'.ljust(10) + 'Name'.ljust(40))
        print(PrintHelpers.colorize(DateTimeUtils.show_timedelta(latest_period.end - latest_period.start).ljust(10), TerminalColors.GREEN) \
            + DateTimeUtils.show_date(latest_period.start).ljust(12) \
            + DateTimeUtils.show_time(latest_period.start).ljust(6) \
            + DateTimeUtils.show_time(latest_period.end).ljust(6) \
            + PrintHelpers.colorize(PrintHelpers.max_width(','.join(latest_task.tags), 20), TerminalColors.BLUE) \
            + PrintHelpers.colorize(PrintHelpers.max_width(','.join(latest_task.ids), 10), TerminalColors.BOLD) \
            + PrintHelpers.max_width(latest_task.description, 40))


# Print total time for given collection of entries
class TotalTimeReport(TaskReportBase):
    def __init__(self, target_time, show_per_day):
        super(TotalTimeReport, self).__init__()
        self.target_time = target_time
        self.show_per_day = show_per_day

    # Gets targetted times (both total and per day)
    def get_targets(self, total_duration, days):
        if self.target_time.target == datetime.timedelta(0):
            return '', ''
        target_total = self.target_time.target
        if self.target_time.is_per_day:
            target_total = target_total * len(days)
        
        total_difference = total_duration - target_total
        return ' (' + DateTimeUtils.show_timedelta(total_difference) + ')', ' (' + DateTimeUtils.show_timedelta(total_difference / len(days)) + ')'

    def print_report(self, collection):
        total_duration = datetime.timedelta(0)
        days = {}
        for task in collection.tasks:
            total_duration += task.duration_total()
            if len(task.periods) > 0 and str(task.periods[0].start.date()) not in days:
                days[str(task.periods[0].start.date())] = 1

        if len(days) == 0:
            return

        target_total, target_per_day = self.get_targets(total_duration, days)
        print('')
        print(' '*31 + 'Total '.ljust(10) + DateTimeUtils.show_timedelta(total_duration) + target_total)
        if self.show_per_day:
            print(' '*31 + 'Per day '.ljust(10) + DateTimeUtils.show_timedelta(total_duration / len(days)) + target_per_day)

# Print graphical report by categories
class CategoriesReport(TaskReportBase):
    def __init__(self, filter_level):
        super(CategoriesReport, self).__init__()
        self.filter_level = filter_level

    def get_categories(self, collection, level):
        tags = {}
        if len(collection.tasks) == 0:
            return tags

        for task in collection.tasks:
            tag_name = task.description
            if len(task.tags) > level:
                tag_name = task.tags[level]
            if tag_name in tags:
                tags[tag_name] += task.duration_total()
            else:
                tags[tag_name] = task.duration_total()
        
        return sorted(tags.items(), key=lambda kv: kv[1], reverse=True)

    def print_report(self, collection):
        tags = self.get_categories(collection, self.filter_level)
        if len(tags) == 0:
            print("Filter did not return any matching item")
            return

        max_duration = next(iter(tags))[1]
        for tag in tags:
            bar_graph = PrintHelpers.get_graph(tag[1], max_duration)
            line = PrintHelpers.colorize(bar_graph, PrintHelpers.get_color())  + ' ' + str(DateTimeUtils.show_timedelta(tag[1])) + ' ' + str(tag[0])
            print(line)
