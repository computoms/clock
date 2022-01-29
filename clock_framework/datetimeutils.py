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
    def parse_time(date, time):
        day_time = datetime.datetime.strptime(time, '%H:%M')
        return datetime.datetime(date.year, date.month, date.day, day_time.hour, day_time.minute, 0)

    @staticmethod
    def get_seconds(timedelta):
        return timedelta.days * 24 * 3600 + timedelta.seconds

    @staticmethod
    def show_timedelta(delta):
        total_seconds = DateTimeUtils.get_seconds(delta)
        hours = total_seconds / 3600
        minutes = (total_seconds - hours * 3600) / 60
        return str(hours).zfill(2) + 'h ' + str(minutes).zfill(2) + 'm'
