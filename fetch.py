from bs4 import BeautifulSoup
import pandas

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

        return self.__to_data_frame((session.post(LectureTimetable.DATA_URL, query_data)))

    def faculty_timetable(self, session):
        weekday_options = WeekdayOptions(self.soup)
        programme_course_options = ProgrammeCourseOptions(self.soup, weekday_options)
        programme_group_options = ProgrammeGroupOptions(self.soup, programme_course_options)
        programme_options = ProgrammeOptions(self.soup, programme_group_options)
        degree_options = DegreeOptions(self.soup, programme_options)
        faculty_options = FacultyOptions(self.soup, degree_options)
        query_data = faculty_options.get_sequence(session, self.soup)

        return self.__to_data_frame((session.post(LectureTimetable.DATA_URL, query_data)))

    def course_timetable(self, session):
        query_data = {}
        query_data.update(CourseOptions().get(self.soup))
        query_data.update(YearOptions().get(self.soup))
        query_data.update(SemesterOptions().get(self.soup))
        query_data.update(DateOptions().get(self.soup))

        return self.__to_data_frame(session.post(LectureTimetable.DATA_URL, query_data))

    def teacher_timetable(self, session):
        query_data = {}
        query_data.update(TeacherOptions().get(self.soup))
        query_data.update(YearOptions().get(self.soup))
        query_data.update(SemesterOptions().get(self.soup))
        query_data.update(DateOptions().get(self.soup))

        return self.__to_data_frame(session.post(LectureTimetable.DATA_URL, query_data))

    def __to_data_frame(self, response):
        return zip(self.__table_headers(response), pandas.read_html(response.text))

    @staticmethod
    def __table_headers(response):
        soup = BeautifulSoup(response.text, 'lxml')
        return [TableHeader(header.text) for header in soup.select(f'h3[class=table-header]')]


class TableHeader:

    DOW_NAME = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
                'Pirmadienis', 'Antradienis', 'Trečiadienis', 'Ketvirtadienis', 'Penktadienis', 'Šeštadienis', 'Sekmadienis']
    DOW_INDEXES = list(range(7)) * (len(DOW_NAME) // 7)
    DOW_MAP = dict(zip(DOW_NAME, DOW_INDEXES))

    def __init__(self, header):
        data = [x.strip() for x in header.split(" ") if len(x) > 1]
        self.dayofweek = self.DOW_MAP[data[0]]
        self.start_date = data[1]
        self.start_date = data[2]









