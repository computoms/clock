import datetime

class DateTimeUtils:
    @staticmethod
    def get_date(line):
        return datetime.datetime.strptime(line[1:11], '%Y-%m-%d')

    @staticmethod
    def is_date(line):
        if line[0] == '[':
            try:
                DateTimeUtils.get_date(line)
                return True
            except ValueError:
                return False

    @staticmethod
    def show_date(date):
        return date.strftime('%Y-%m-%d')

    @staticmethod
    def show_time(date):
        return date.strftime('%H:%M')

    @staticmethod
    def parse_time(date, time):
        day_time = datetime.datetime.strptime(time, '%H:%M')
        return datetime.datetime(date.year, date.month, date.day, day_time.hour, day_time.minute, 0)

    @staticmethod
    def parse_duration(duration):
        s = duration.split(':')
        if len(s) == 0:
            return datetime.timedelta(0)
        if len(s) == 1:
            return datetime.timedelta(0, int(s) * 3600)
        if len(s) == 2:
            return datetime.timedelta(0, int(s[0]) * 3600 + int(s[1]) * 60)
        if len(s) == 3:
            return datetime.timedelta(0, int(s[0]) * 3600 + int(s[1]) * 60 + int(s[2]))

        return datetime.timedelta(0)

    @staticmethod
    def get_seconds(timedelta):
        return timedelta.days * 24 * 3600 + timedelta.seconds

    @staticmethod
    def show_timedelta(delta):
        total_seconds = DateTimeUtils.get_seconds(delta)
        hours = int(total_seconds / 3600)
        minutes = int((total_seconds - hours * 3600) / 60)
        return str(hours).zfill(2) + 'h ' + str(minutes).zfill(2) + 'm'

    
