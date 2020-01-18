import datetime


class WeekIterator:

    def __init__(self, weekday, starting_week_odd=True):
        self.date_from = self.next_weekday(self.to_datetime(weekday.date_from), weekday.day_of_week)
        self.date_to = self.previous_weekday(self.to_datetime(weekday.date_to), weekday.day_of_week)
        self.day_of_week = weekday.day_of_week
        self.date_current = self.date_from
        self.is_odd = starting_week_odd

    def iterate(self):
        while self.date_current <= self.date_to:
            yield True
            self.next_week()
        return False

    def next_week(self):
        self.is_odd = not self.is_odd
        self.date_current = self.date_current + datetime.timedelta(7)

    def to_datetime(self, date):
        return datetime.date(*[int(x) for x in date.split('-')])

    def next_weekday(self, date, day_of_week):
        days_ahead = day_of_week - date.weekday()
        return date + datetime.timedelta(days_ahead)

    def previous_weekday(self, date, day_of_week):
        days_ahead = date.weekday() - day_of_week
        return date - datetime.timedelta(days_ahead)
