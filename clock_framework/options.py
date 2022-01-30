from datetime import datetime
from datetime import timedelta

from clock_framework.datetimeutils import DateTimeUtils


class Switch:
    def __init__(self, short, long, expects_arg, description):
        self.short = short
        self.long = long
        self.expects_argument = expects_arg
        self.is_active = False
        self.value = None
        self.description = description
    
    def default_value(self, value):
        new_switch = Switch(self.short, self.long, self.expects_argument, self.description)
        new_switch.value = value
        return new_switch

    def corresponds_to(self, arg):
        return arg in (self.short, self.long)

class Command:
    def __init__(self, command, description):
        self.command = command
        self.description = description
        
class TargetTime:
    def __init__(self, target, is_per_day):
        self.target = target
        self.is_per_day = is_per_day

class Commands:
    add = Command('add', 'Adds a new entry')
    show = Command('show', 'Shows statistics')
    stop = Command('stop', 'Stops current entry or finishes the day')
    
class ClockOptions:
    def __init__(self):
        self.arguments = []
        self.command = Commands.add

        self.help = Switch('-h', '--help', False, 'Shows this help message')
        self.at = Switch('-a', '--at', True, '<add> Specify a time (format HH:MM) of a new entry').default_value(datetime.now().strftime('%H:%M'))
        self.edit_current = Switch('-c', '--current', False, '<add> Modify the description of the current entry')
        self.file = Switch('-f', '--file', True, 'Speficy the file to store time entries. Default is ./clock.txt').default_value('./clock.txt')
        self.today = Switch('-t', '--today', False, '<show> Show only entries from today')
        self.this_week = Switch('-w', '--week', False, '<show> Show only entries from the current week')
        self.from_filter = Switch('-s', '--from', True, '<show> Include entries with start date later or equal to given date (format YYYY-mm-dd)')
        self.to_filter = Switch('-e', '--to', True, '<show> Include entries with start date earlier or equal to given date (format YYYY-mm-dd)')
        self.target_time = Switch('-T', '--target', True, '<show> Sets expected target time (format HH:MM) and computes the difference with actual times in the reports')
        self.target_time_per_day = Switch('-D', '--target-per-day', True, '<show> Sets expected target time per day (format HH:MM) and computes the difference with actual times in the reports')

        self.switch_list = [self.help, self.file, self.at, self.edit_current, self.today, self.this_week, self.from_filter, self.to_filter, self.target_time, self.target_time_per_day]
        self.command_list = [Commands.add, Commands.show, Commands.stop]

    def get_target_time(self):
        if self.target_time.is_active:
            return TargetTime(DateTimeUtils.parse_duration(self.target_time.value), False)
        elif self.target_time_per_day.is_active:
            return TargetTime(DateTimeUtils.parse_duration(self.target_time_per_day.value), True)
        return TargetTime(timedelta(0), False)

    def is_command(self, word):
        return word in [cmd.command for cmd in self.command_list]

    def get_command(self, word):
        for cmd in self.command_list:
            if cmd.command == word:
                return cmd
        return None

    def get_switch(self, arg):
        for s in self.switch_list:
            if s.corresponds_to(arg):
                return s
        return None

    def extract_command(self, arguments):
        if len(arguments) > 1 and self.is_command(arguments[1]):
            self.command = self.get_command(arguments[1])
            return arguments[2:]
        return arguments[1:]

    def parse(self, arguments):
        arguments = self.extract_command(arguments)
        i = 0
        while i < len(arguments):
            arg = arguments[i]
            s = self.get_switch(arg)
            if s is not None:
                s.is_active = True
                if s.expects_argument and len(arguments) > (i + 1):
                    i = i + 1
                    s.value = arguments[i]
            else:
                self.arguments.append(arg)
            i = i + 1

    def show_help(self):
        print('Usage: ./clock <command> [options] [description]')
        print('')
        print('COMMANDS')
        for cmd in self.command_list:
            print('     ' + str(cmd.command).ljust(22, ' ') + cmd.description)
        print('')
        print('OPTIONS')
        for opt in self.switch_list:
            print('     ' + opt.short + ', ' + str(opt.long).ljust(18, ' ') + opt.description)
        print('')
        print('EXAMPLES')
        print('     Adds entry "Prototype implementation" with two ordered tags "+myapp" and "+coding" and one id ".456"')
        print('')
        print('       $ ./clock add Prototype implementation +myapp +coding .456')
        print('')
        print('     Adds new entry starting today at 09:50 "Adding new feature" with id ".457"')
        print('')
        print('       $ ./clock Adding new feature .457 --at 09:50')
        print('')
        print('     Updates current entry description with "Updating description of last line" with one tag "+myapp"')
        print('')
        print('       $ ./clock -c Updating description of the last line +myapp')
        print('')
        print('     Shows statistics for today')
        print('')
        print('       $ ./clock show --today')
        print('')
        print('     Shows statistics for entries with tag "+myapp"')
        print('')
        print('       $ ./clock show +myapp')
        print('')
        print('     Shows statistics for entries with tag "+myapp" for the period from 2022-01-01 to 2022-01-31')
        print('')
        print('       $ ./clock show --from 2022-01-01 --to 2022-01-31 +myapp')



