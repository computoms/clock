from datetime import datetime


class Switch:
    def __init__(self, short, long, expects_arg):
        self.short = short
        self.long = long
        self.expects_argument = expects_arg
        self.is_active = False
        self.value = None
    
    def default_value(self, value):
        new_switch = Switch(self.short, self.long, self.expects_argument)
        new_switch.value = value
        return new_switch

    def corresponds_to(self, arg):
        return arg in (self.short, self.long)

class Commands:
    add = 'add'
    show = 'show'
    stop = 'stop'

    list = [add, show, stop]
    
class ClockOptions:
    def __init__(self):
        self.arguments = []
        self.command = Commands.add

        self.at = Switch('-a', '--at', True).default_value(datetime.now().strftime('%H:%M'))
        self.edit_current = Switch('-c', '--current', False)
        self.file = Switch('-f', '--file', True).default_value('./clock.txt')
        self.today = Switch('-t', '--today', False)
        self.this_week = Switch('-w', '--week', False)
        self.from_filter = Switch('-s', '--from', True)
        self.to_filter = Switch('-e', '--to', True)

        self.switch_list = [self.at, self.edit_current, self.file, self.today, self.this_week, self.from_filter, self.to_filter]

    def is_command(self, word):
        return word in Commands.list

    def get_switch(self, arg):
        for s in self.switch_list:
            if s.corresponds_to(arg):
                return s
        return None

    def extract_command(self, arguments):
        if len(arguments) > 1 and self.is_command(arguments[1]):
            self.command = arguments[1]
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
