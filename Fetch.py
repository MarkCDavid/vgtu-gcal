from datetime import date

from bs4 import BeautifulSoup

import utility


class TimetableOptions:

    def __init__(self, id, prompt):
        self.id = id
        self.prompt = prompt

    @staticmethod
    def selector(options):
        return options['name']

    def get(self, soup):
        options = utility.select2_extractor(soup, self.id)
        selection = utility.select_closest_prompt(self.prompt, options['options'],
                                                  self.default, TimetableOptions.selector)
        return {options['name']: selection['value']}

    def default(self, options):
        raise NotImplemented()


class GroupOptions(TimetableOptions):

    def __init__(self):
        super().__init__('timetable-gr_kodas', 'Group: ')

    def default(self, options):
        return None


class YearOptions(TimetableOptions):

    def __init__(self):
        super().__init__('timetable-m_metai', 'Year: ')

    def default(self, options):
        return options[1]


class SemesterOptions(TimetableOptions):

    def __init__(self):
        super().__init__('timetable-sesija_pav', 'Semester: ')

    def default(self, options):
        spring_semester = range(2, 8)
        current_month = date.today().month
        return options[2 if current_month in spring_semester else 1]


class DateOptions(TimetableOptions):

    def __init__(self):
        super().__init__('timetable-data', '')

    def get(self, soup):
        return {soup.find('input', id=self.id)['name']: utility.date_prompt()}


class LectureTypeOptions(TimetableOptions):

    def __init__(self):
        super().__init__('timetable-pask_rus', 'Lecture type: ')

    def default(self, options):
        return options[0]


class CourseOptions(TimetableOptions):

    def __init__(self):
        super().__init__('timetable-dal_pavad', 'Course: ')

    def default(self, options):
        return options[1]


class TeacherOptions(TimetableOptions):

    def __init__(self):
        super().__init__('timetable-paz_id', 'Teacher: ')

    def default(self, options):
        return options[1]


class LectureTimetable:
    BASE_URL = 'https://mano.vgtu.lt/timetable/site/search-form'
    DATA_URL = 'https://mano.vgtu.lt/timetable/site/search-ajax'
    INFO_URL = 'https://mano.vgtu.lt/timetable/site/timetableinfo'

    @staticmethod
    def group_timetable(session):
        response = session.get(LectureTimetable.BASE_URL)
        soup = BeautifulSoup(response.text, 'lxml')

        query_data = {}
        query_data.update(GroupOptions().get(soup))
        query_data.update(YearOptions().get(soup))
        query_data.update(SemesterOptions().get(soup))
        query_data.update(DateOptions().get(soup))
        query_data.update(LectureTypeOptions().get(soup))

        return session.post(LectureTimetable.DATA_URL, query_data)

    @staticmethod
    def course_timetable(session):
        response = session.get(LectureTimetable.BASE_URL)
        soup = BeautifulSoup(response.text, 'lxml')

        query_data = {}
        query_data.update(CourseOptions().get(soup))
        query_data.update(YearOptions().get(soup))
        query_data.update(SemesterOptions().get(soup))
        query_data.update(DateOptions().get(soup))

        return session.post(LectureTimetable.DATA_URL, query_data)

    @staticmethod
    def teacher_timetable(session):
        response = session.get(LectureTimetable.BASE_URL)
        soup = BeautifulSoup(response.text, 'lxml')

        query_data = {}
        query_data.update(TeacherOptions().get(soup))
        query_data.update(YearOptions().get(soup))
        query_data.update(SemesterOptions().get(soup))
        query_data.update(DateOptions().get(soup))

        return session.post(LectureTimetable.DATA_URL, query_data)
