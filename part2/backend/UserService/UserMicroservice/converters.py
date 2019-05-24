import datetime
import time


class BoolConverter:
    regex = '(True|False)'

    def to_python(self, value):
        if value == 'True':
            return True
        return False

    def to_url(self, value):
        if value:
            return 'True'
        return 'False'


class DateConverter:
    regex = '[0-9]{4}\-[0-9]{2}\-[0-9]{2}'

    def to_python(self, value):
        return datetime.datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value.isoformat()


class TimeConverter:
    regex = '[0-9]{2}:[0-9]{2}:[0-9]{2}'

    def to_python(self, value):
        return datetime.datetime.strptime(value, '%H:%M:%S')

    def to_url(self, value):
        return value.isoformat(timespec='auto')

