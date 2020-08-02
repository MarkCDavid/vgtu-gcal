from datetime import date

import utility
import select2


class TimetableOptions:

    def __init__(self, id):
        self.id = id

    @staticmethod
    def selector(option):
        return option.name

    def get(self, soup):
        selection = select2.Selection(self.id, soup)
        choice = utility.select_closest_prompt(f'{selection.name}:', selection.options,
                                               self.default, TimetableOptions.selector)
        return {selection.query_name: choice.value}

    def default(self, options):
        return options[0]


class GroupOptions(TimetableOptions):

    def __init__(self):
        super().__init__('gr_kodas')

    def default(self, options):
        return None


class YearOptions(TimetableOptions):

    def __init__(self):
        super().__init__('m_metai')


class SemesterOptions(TimetableOptions):

    def __init__(self):
        super().__init__('sesija_pav')


class DateOptions(TimetableOptions):

    def __init__(self):
        super().__init__('data')

    def get(self, soup):
        return {soup.find('input', id=f'timetable-{self.id}')['name']: utility.date_prompt()}


class LectureTypeOptions(TimetableOptions):

    def __init__(self):
        super().__init__('pask_rus')


class CourseOptions(TimetableOptions):

    def __init__(self):
        super().__init__('dal_pavad')


class TeacherOptions(TimetableOptions):

    def __init__(self):
        super().__init__('paz_id')
