class Timetable:

    def __init__(self):
        self.weekdays = []

    def AddWeekday(self, weekday):
        self.weekdays.append(weekday)


class TimetableWeekday:

    def __init__(self):
        self.events = []

    def UpdateData(self, weekday_data, day_of_week_translation):
        self.day_of_week = day_of_week_translation[weekday_data[0]]
        self.date_from = weekday_data[1]
        self.date_to = weekday_data[2]

    def AddEvent(self, event):
        self.events.append(event)


class TimetableEvent:

    def Update(self, entry):
        self.Lecture = entry[0]
        self.Group = entry[1]
        self.Time = entry[2]
        self.Week = entry[3]
        self.Subgroup = entry[4]
        self.Subject = entry[5]
        self.Auditory = entry[6]
        self.Lecturer = entry[7]
        self.Type = entry[8]
