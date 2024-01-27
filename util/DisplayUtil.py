from datetime import datetime
import calendar


def date_to_day(date):
    datetime_object = datetime.strptime(date, '%Y-%m-%d')
    return calendar.day_name[datetime_object.weekday()]
