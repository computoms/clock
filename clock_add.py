from datetime import date
from datetime import datetime
import sys

# Parse command line options

class Options:
    def __init__(self):
        self.at = datetime.now().strftime('%H:%M')
        self.current = False
        self.description = ''
        self.file = './clock.txt'

    def parse(self, arguments):
        i = 0
        while i < len(arguments):
            arg = arguments[i]
            if arg in ('-a', '--at'):           # Add item at given time
                i = i + 1
                self.at = arguments[i]
            elif arg in ('-c', '--current'):    # Replace current line by new description
                self.current = True
            elif arg in ('-f', '--file'):       # Use different source file
                i = i + 1
                self.file = arguments[i]
            else:
                self.description += arg + ' '
            i = i + 1

opt = Options()
opt.parse(sys.argv[1:])


def date_exists(file):
    today = date.today().strftime("%Y-%m-%d")
    try:
        with open(file, "r") as f:
            for l in f:
                if l[0] == '[' and l[1:11] == today:
                    return True
    except Exception:
        return False

# Add today's date if necessary
if not date_exists(opt.file):
    with open(opt.file, "a") as f:
        today = date.today().strftime("[%Y-%m-%d]")
        f.write(today + "\n")


# Add time and concatenate all arguments
description = opt.at + ' ' + opt.description + '\n'

if opt.current:
    lines = open(opt.file, 'r').readlines()
    description = lines[-1][0:5] + ' ' + opt.description + '\n'
    lines[-1] = description
    open(opt.file, 'w').writelines(lines)
else:
    with open(opt.file, 'a') as f:
        f.write(description)