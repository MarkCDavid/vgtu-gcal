import utils.stringutils as stringutils
import utils.csvutils as csvutils
from utils.weekiterator import WeekIterator

headings = ["Subject", "Start Date", "Start Time", "End Date", "End Time", "All Day Event", "Location", "Description"]
header = ','.join(headings)


class Options:

    def __init__(self, simple, include_subgroup):
        self.simple = simple
        self.include_subgroup = include_subgroup

    @staticmethod
    def Default():
        return Options(False, True)


def csv_gcal_timetableevent(event, date, options):

    def format_subject(event, options):
        subject = f"{stringutils.remove_parentheses(event.Subject) if options.simple else event.Subject}".strip()
        group = f" gr. {event.Subgroup}" if options.include_subgroup else ""
        subject_type = f"({event.Type})"
        return f"{(subject + group).strip()} {subject_type}"

    return csvutils.csv_entry(
            format_subject(event, options),
            str(date),
            event.Time[0],
            str(date),
            event.Time[1],
            "False",
            event.Auditory,
            event.Lecturer
        )


def is_entry_valid(event, odd_week):
    byweekly = event.Week != ""
    if byweekly:
        is_odd_week = int(event.Week) % 2 == 1
        return is_odd_week == odd_week
    return True


def csv_gcal_weekday(weekday, week, options):
    gcal_weekday = ""
    for event in weekday.events:
        if is_entry_valid(event, week.is_odd):
            gcal_weekday += csv_gcal_timetableevent(event, week.date_current, options)
    return gcal_weekday


def csv_gcal(timetable, filename, options):
    gcal = header + "\n"
    for weekday in timetable.weekdays:
        week = WeekIterator(weekday)
        for handle_week in week.iterate():
            if handle_week:
                gcal += csv_gcal_weekday(weekday, week, options)

    with open(filename, 'w', encoding="utf-8") as f:
        f.write(gcal)
