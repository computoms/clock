import configparser
from clock_tracking.datetimeutils import DateTimeUtils

class ClockConfig:
    def __init__(self, file):
        self.config = configparser.ConfigParser()
        self.config.read_file(file)

    def target(self):
        return DateTimeUtils.parse_duration(self.config.get('Target', 'total_target', fallback='00:00'))
    def target_per_day(self):
        return DateTimeUtils.parse_duration(self.config.get('Target', 'target_per_day', fallback='00:00'))
    def file(self):
        return self.config.get('File', 'file', fallback='')
