from datetime import date
from datetime import datetime
import sys

file = "./clock.txt"

def date_exists():
    today = date.today().strftime("%Y-%m-%d")
    with open(file, "r") as f:
        for l in f:
            if l[0] == '[' and l[1:11] == today:
                return True
    
    return False

# Add today's date if necessary
if not date_exists():
    with open(file, "a") as f:
        today = date.today().strftime("[%Y-%m-%d]")
        f.write(today + "\n")

# Add time and concatenate all arguments
description = datetime.now().strftime("%H:%M") + ' '
for i, arg in enumerate(sys.argv[1:]):
    description += arg + ' '
description += '\n'

with open(file, "a") as f:
    f.write(description)