import datetime
from xmlrpc.client import DateTime
from clock_tracking.datetimeutils import DateTimeUtils
from clock_tracking.colors import TerminalColors
import os

class PrintHelpers:
    color_index = -1

    @staticmethod
    def get_graph(time, totaltime, char_width_total):
        char_width = DateTimeUtils.get_seconds(time) * char_width_total / DateTimeUtils.get_seconds(totaltime)
        result = [u'\u2588' for i in range(int(char_width))]
        result.extend([' ' for i in range(int(char_width), char_width_total)])
        return ''.join(result)

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

# Prints periods in chronological order
class DetailsReport(TaskReportBase):
    def __init__(self):
        super(DetailsReport, self).__init__()

    def print_report(self, collection):
        periods = []
        for task in collection.tasks:
            for p in task.periods:
                periods.append([p, task])

        periods = sorted(periods, key=lambda t: t[0].start)
        total_width = os.get_terminal_size().columns
        remaining_width = total_width - (10 + 12 + 6 + 6 + 20 + 10)
        if remaining_width < 0:
            print("Terminal is too small to show details.")
            exit

        print(str('Duration').ljust(10) + 'Date'.ljust(12) + 'Start'.ljust(6) + 'Stop'.ljust(6) + 'Tags'.ljust(20) + 'IDs'.ljust(10) + 'Name'.ljust(remaining_width))
        for kv in periods:
            p = kv[0]
            print(PrintHelpers.colorize(DateTimeUtils.show_timedelta(p.end - p.start).ljust(10), TerminalColors.GREEN) \
                + DateTimeUtils.show_date(p.start).ljust(12) \
                + DateTimeUtils.show_time(p.start).ljust(6) \
                + DateTimeUtils.show_time(p.end).ljust(6) \
                + PrintHelpers.colorize(PrintHelpers.max_width(','.join(kv[1].tags), 20), TerminalColors.BLUE) \
                + PrintHelpers.colorize(PrintHelpers.max_width(','.join(kv[1].ids), 10), TerminalColors.BOLD) \
                + PrintHelpers.max_width(kv[1].description, remaining_width))

# Print total time for given collection of entries
class TotalTimeReport(TaskReportBase):
    def __init__(self, target_time):
        super(TotalTimeReport, self).__init__()
        self.target_time = target_time

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
        print(PrintHelpers.colorize(DateTimeUtils.show_timedelta(total_duration), TerminalColors.GREEN) + target_total + ' Total')
        if len(days) > 1:
            print(PrintHelpers.colorize(DateTimeUtils.show_timedelta(total_duration / len(days)), TerminalColors.GREEN) + target_per_day + ' Per day')

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

    def get_graph_length(self, max_tag_length):
        graph_length = os.get_terminal_size().columns - max_tag_length - 10
        if graph_length > 100:
            graph_length = 100
        return graph_length

    def print_report(self, collection):
        tags = self.get_categories(collection, self.filter_level)
        if len(tags) == 0:
            print("Filter did not return any matching item")
            return

        max_tag_length = len(max(tags, key=lambda k: len(k[0]))[0]) + 1
        if max_tag_length == 0:
            max_tag_length = 20

        max_duration = next(iter(tags))[1]
        for tag in tags:
            bar_graph = PrintHelpers.get_graph(tag[1], max_duration, self.get_graph_length(max_tag_length))
            line = PrintHelpers.colorize(str(DateTimeUtils.show_timedelta(tag[1])), TerminalColors.GREEN) + ' ' + str(tag[0]).ljust(max_tag_length) \
                + PrintHelpers.colorize(bar_graph, PrintHelpers.get_color())
            print(line)

class DayTimelineReport(TaskReportBase):
    def __init__(self):
        super(DayTimelineReport, self).__init__()
    
    def print_report(self, collection):
        periods = []
        for task in collection.tasks:
            for p in task.periods:
                periods.append([p, task])

        periods = sorted(periods, key=lambda t: t[0].start)

        total_width = os.get_terminal_size().columns
        if total_width < 60:
            print("Terminal is too small to show timeline")
            return
        hour_width = int((total_width - 40) / 11)

        print('Description'.ljust(40) + '8'.ljust(hour_width) + '9'.ljust(hour_width) + '10'.ljust(hour_width) \
            + '11'.ljust(hour_width) + '12'.ljust(hour_width) + '13'.ljust(hour_width) + '14'.ljust(hour_width) \
            + '15'.ljust(hour_width) + '16'.ljust(hour_width) + '17'.ljust(hour_width) + '18'.ljust(hour_width))
        for kv in periods:
            p = kv[0]
            seconds_start = (p.start - datetime.datetime(datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day, 8)).seconds
            seconds_end = seconds_start + (p.end - p.start).seconds
            start = int(seconds_start * hour_width / 3600)
            length = int((seconds_end - seconds_start) * hour_width / 3600)
            description = PrintHelpers.max_width(kv[1].description, 40)
            line = PrintHelpers.colorize(description + ' '*start + u'\u2588'*length, PrintHelpers.get_color())
            print(line)

