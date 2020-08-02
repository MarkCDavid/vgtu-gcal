from bs4 import BeautifulSoup

import utility
from TimetableOptions.Regular import TimetableOptions


class SequentialOptions(TimetableOptions):
    INFO_URL = 'https://mano.vgtu.lt/timetable/site/timetableinfo'

    def __init__(self, id, prompt, soup, successor=None):
        super().__init__(id, prompt)
        self.successor = successor
        self.request_id = utility.select2_table_name(soup, id)
        self.request_value = None

    def get_sequence(self, session, soup, params=None):
        _, self.request_value = super().get(soup).popitem()
        result = {self.request_id: self.request_value}

        params, soup = self.__next(session, params)

        if self.successor is not None:
            result.update(self.successor.get_sequence(session, soup, params))

        return result

    def default(self, options):
        return options[1]

    def __next(self, session, params):
        params = self.update_params(params if params is not None else self.__default_params())
        return params, BeautifulSoup(session.post(SequentialOptions.INFO_URL, params).text, 'lxml')

    def update_params(self, params):
        params['id'] = self.request_id
        params['val'] = self.request_value
        return params

    @staticmethod
    def __default_params():
        return {
            'id': '',
            'val': '',
            'faculty': '',
            'grupe': '',
        }


class FacultyOptions(SequentialOptions):

    def __init__(self, soup, successor=None):
        super().__init__('timetable-pad_id', 'Faculty: ', soup, successor)

    def default(self, options):
        return options[1]

    def update_params(self, params):
        super().update_params(params)
        params['faculty'] = self.request_value
        return params


class DegreeOptions(SequentialOptions):

    def __init__(self, soup, successor=None):
        super().__init__('timetable-pakopa', 'Degree: ', soup, successor)

    def default(self, options):
        return options[1]


class ProgrammeOptions(SequentialOptions):

    def __init__(self, soup, successor=None):
        super().__init__('timetable-prog_id', 'Programme: ', soup, successor)

    def default(self, options):
        return options[1]


class ProgrammeGroupOptions(SequentialOptions):

    def __init__(self, soup, successor=None):
        super().__init__('timetable-dal_kodas', 'Group: ', soup, successor)

    def default(self, options):
        return options[1]

    def update_params(self, params):
        super().update_params(params)
        params['grupe'] = self.request_value
        return params


class ProgrammeCourseOptions(SequentialOptions):

    def __init__(self, soup, successor=None):
        super().__init__('timetable-kursas', 'Course: ', soup, successor)

    def default(self, options):
        return options[1]


class WeekdayOptions(SequentialOptions):

    def __init__(self, soup, successor=None):
        super().__init__('timetable-dien_id', 'Weekday: ', soup, successor)

    def default(self, options):
        return options[1]