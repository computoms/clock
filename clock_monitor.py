#!/usr/bin/env python
from time import sleep
import sys
import datetime
import os

def get_app_name():
    if sys.platform == 'darwin':
        from AppKit import NSWorkspace
        return NSWorkspace.sharedWorkspace().frontmostApplication().localizedName()
    else:
        return "Unsupported Platform"

def parse_last_name(line):
    return line[6:].replace('\n', '')

def add_name(filename, name):
    #os.system('python ./clock_add.py ' + name)
    # TODO use clock_add.py but with different filename
    pass
    # line = str(datetime.datetime.now().hour).zfill(2) + ':' + str(datetime.datetime.now().minute).zfill(2) + ' ' + name + '\n'
    # f = open(filename, 'a')
    # f.write(line)
    # f.close()

def get_last_line(filename):
    line = ''
    try:
        f = open(filename, 'r')
        for line in f:
            pass
        f.close()
    except Exception:
        print("File " + str(filename) + " not found.")
    return line


file = './clock-monitor.txt'
line = get_last_line(file)
last_name = parse_last_name(line)
current_name = get_app_name()

if last_name != current_name:
    add_name(file, current_name)
    print("Added " + current_name)
