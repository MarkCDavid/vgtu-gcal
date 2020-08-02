from bs4 import BeautifulSoup

import utility
from TimetableOptions.Regular import TimetableOptions


class SequentialOptions(TimetableOptions):
    INFO_URL = 'https://mano.vgtu.lt/timetable/site/timetableinfo'

    def __init__(self, id, soup, successor=None):
        super().__init__(id)
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
        super().__init__('pad_id', soup, successor)

    def update_params(self, params):
        super().update_params(params)
        params['faculty'] = self.request_value
        return params


class DegreeOptions(SequentialOptions):

    def __init__(self, soup, successor=None):
        super().__init__('pakopa', soup, successor)


class ProgrammeOptions(SequentialOptions):

    def __init__(self, soup, successor=None):
        super().__init__('prog_id', soup, successor)


class ProgrammeGroupOptions(SequentialOptions):

    def __init__(self, soup, successor=None):
        super().__init__('dal_kodas', soup, successor)

    def update_params(self, params):
        super().update_params(params)
        params['grupe'] = self.request_value
        return params


class ProgrammeCourseOptions(SequentialOptions):

    def __init__(self, soup, successor=None):
        super().__init__('kursas', soup, successor)


class WeekdayOptions(SequentialOptions):

    def __init__(self, soup, successor=None):
        super().__init__('dien_id', soup, successor)