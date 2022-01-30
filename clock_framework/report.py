import datetime
from datetimeutils import DateTimeUtils
from colors import TerminalColors

class TaskReport:
    def __init__(self, task_collection):
        self.collection = task_collection
        self.graph_width = 40

    def get_graph(self, time, totaltime):
        char_width = DateTimeUtils.get_seconds(time) * self.graph_width / DateTimeUtils.get_seconds(totaltime)
        result = [u'\u2588' for i in range(char_width)]
        result.extend([' ' for i in range(char_width, self.graph_width)])
        return ''.join(result)

    def print_all(self):
        for task in self.collection.tasks:
            desc = task.description + " "
            for tag in task.tags:
                desc += tag + " "
            print(desc)
            for period in task.periods:
                print(" . " + str(period.start) + " --> " + str(period.end))

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
        return tags

    def get_color(self, index):
        if index == 0:
            return TerminalColors.BLUE
        if index == 1:
            return TerminalColors.CYAN
        return TerminalColors.GREEN

    def increase_circular_index(self, index):
        if index + 1 > 2:
            return 0
        return index + 1

    def show(self, level):
        tags = self.get_categories(level)
        tags = sorted(tags.items(), key=lambda kv: kv[1], reverse=True) # Sort result by duration
        if len(tags) == 0:
            print("Filter did not return any matching item")
            return

        max_duration = next(iter(tags))[1]
        index = 0
        for tag in tags:
            bar_graph = self.get_graph(tag[1], max_duration)
            line = self.get_color(index) + bar_graph + TerminalColors.END + ' ' + str(DateTimeUtils.show_timedelta(tag[1])) + ' ' + str(tag[0])
            index = self.increase_circular_index(index)
            print(line)

    def print_total_time(self):
        total_duration = datetime.timedelta(0)
        days = {}
        for task in self.collection.tasks:
            total_duration += task.duration_total()
            if len(task.periods) > 0 and str(task.periods[0].start.date()) not in days:
                days[str(task.periods[0].start.date())] = 1

        if len(days) == 0:
            return
        per_day = total_duration / len(days)

        print("Total " + DateTimeUtils.show_timedelta(total_duration) + " (" + DateTimeUtils.show_timedelta(per_day) + " per day)")
