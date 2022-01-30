from datetime import datetime

class Commands:
    add = 'add'
    show = 'show'
    stop = 'stop'

    list = [add, show, stop]

class ClockOptions:
    def __init__(self):
        self.at = datetime.now().strftime('%H:%M')
        self.edit_current = False
        self.arguments = []
        self.file = './clock.txt'
        self.command = 'add'
        self.today = False

    def is_command(self, word):
        return word in Commands.list

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
            if arg in ('-a', '--at'):           # Add item at given time
                i = i + 1
                self.at = arguments[i]
            elif arg in ('-c', '--current'):    # Replace current line by new description
                self.edit_current = True
            elif arg in ('-f', '--file'):       # Use different source file
                i = i + 1
                self.file = arguments[i]
            elif arg in ('-t', '--today'):      # Filter issues by today
                self.today = True
            else:
                self.arguments.append(arg)
            i = i + 1
