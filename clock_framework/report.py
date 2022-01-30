import datetime
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

class TaskReportBase(object):
    def __init__(self, task_collection):
        self.collection = task_collection

    def print_report(self):
        print('')

# Print details of all entries in collection
class DetailsReport(TaskReportBase):
    def __init__(self, task_collection):
        super(DetailsReport, self).__init__(task_collection)

    def print_report(self):
        for task in self.collection.tasks:
            desc = task.description + ' '
            for tag in task.tags:
                desc += tag + ' '
            print(desc)
            for p in task.periods:
                print('  . ' + DateTimeUtils.show_date(p.start) + ' --> ' + DateTimeUtils.show_date(p.end)) + ' = ' + DateTimeUtils.show_timedelta(p.end - p.start)

# Print total time for given collection of entries
class TotalTimeReport(TaskReportBase):
    def __init__(self, task_collection, target_time):
        super(TotalTimeReport, self).__init__(task_collection)
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

    def print_report(self):
        total_duration = datetime.timedelta(0)
        days = {}
        for task in self.collection.tasks:
            total_duration += task.duration_total()
            if len(task.periods) > 0 and str(task.periods[0].start.date()) not in days:
                days[str(task.periods[0].start.date())] = 1

        if len(days) == 0:
            return

        target_total, target_per_day = self.get_targets(total_duration, days)
        print('     Total '.ljust(15) + DateTimeUtils.show_timedelta(total_duration) + target_total)
        print('     Per day '.ljust(15) + DateTimeUtils.show_timedelta(total_duration / len(days)) + target_per_day)

# Print graphical report by categories
class CategoriesReport(TaskReportBase):
    def __init__(self, task_collection, filter_level):
        super(CategoriesReport, self).__init__(task_collection)
        self.filter_level = filter_level

    def get_categories(self, level):
        tags = {}
        if len(self.collection.tasks) == 0:
            return tags

        for task in self.collection.tasks:
            tag_name = task.description
            if len(task.tags) > level:
                tag_name = task.tags[level]
            if tag_name in tags:
                tags[tag_name] += task.duration_total()
            else:
                tags[tag_name] = task.duration_total()
        
        return sorted(tags.items(), key=lambda kv: kv[1], reverse=True)

    def print_report(self):
        tags = self.get_categories(self.filter_level)
        if len(tags) == 0:
            print("Filter did not return any matching item")
            return

        max_duration = next(iter(tags))[1]
        for tag in tags:
            bar_graph = PrintHelpers.get_graph(tag[1], max_duration)
            line = PrintHelpers.get_color() + bar_graph + TerminalColors.END + ' ' + str(DateTimeUtils.show_timedelta(tag[1])) + ' ' + str(tag[0])
            print(line)
