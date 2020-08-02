from bs4 import BeautifulSoup

from TimetableOptions.Regular import DateOptions, SemesterOptions, YearOptions, GroupOptions, LectureTypeOptions, \
    CourseOptions, TeacherOptions
from TimetableOptions.Sequential import WeekdayOptions, ProgrammeCourseOptions, ProgrammeGroupOptions, ProgrammeOptions, \
    DegreeOptions, FacultyOptions


class LectureTimetable:
    BASE_URL = 'https://mano.vgtu.lt/timetable/site/search-form'
    DATA_URL = 'https://mano.vgtu.lt/timetable/site/search-ajax'

    def __init__(self, session):
        response = session.get(LectureTimetable.BASE_URL)
        self.soup = BeautifulSoup(response.text, 'lxml')

    def group_timetable(self, session):
        query_data = {}

        query_data.update(GroupOptions().get(self.soup))
        query_data.update(YearOptions().get(self.soup))
        query_data.update(SemesterOptions().get(self.soup))
        query_data.update(DateOptions().get(self.soup))
        query_data.update(LectureTypeOptions().get(self.soup))

        return session.post(LectureTimetable.DATA_URL, query_data)

    def faculty_timetable(self, session):
        weekday_options = WeekdayOptions(self.soup)
        programme_course_options = ProgrammeCourseOptions(self.soup, weekday_options)
        programme_group_options = ProgrammeGroupOptions(self.soup, programme_course_options)
        programme_options = ProgrammeOptions(self.soup, programme_group_options)
        degree_options = DegreeOptions(self.soup, programme_options)
        faculty_options = FacultyOptions(self.soup, degree_options)
        query_data = faculty_options.get_sequence(session, self.soup)

        return session.post(LectureTimetable.DATA_URL, query_data)

    def course_timetable(self, session):
        query_data = {}
        query_data.update(CourseOptions().get(self.soup))
        query_data.update(YearOptions().get(self.soup))
        query_data.update(SemesterOptions().get(self.soup))
        query_data.update(DateOptions().get(self.soup))

        return session.post(LectureTimetable.DATA_URL, query_data)

    def teacher_timetable(self, session):
        query_data = {}
        query_data.update(TeacherOptions().get(self.soup))
        query_data.update(YearOptions().get(self.soup))
        query_data.update(SemesterOptions().get(self.soup))
        query_data.update(DateOptions().get(self.soup))

        return session.post(LectureTimetable.DATA_URL, query_data)

