from sys import path as syspath
from os import path as ospath

syspath.append(ospath.dirname(ospath.realpath(__file__)))
from clock_tracking.clock import Clock

Clock.run()