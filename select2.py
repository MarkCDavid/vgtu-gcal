from bs4 import BeautifulSoup
import json


class Option:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Selection:
    def __init__(self, id, soup):
        self.id = id
        self.query_name = f'Timetable[{id.upper()}]'

        select2_div = soup.select(f'div[class*=field-timetable-{id}]')[0]
        self.required = 'required' in select2_div['class']
        self.name = select2_div.find('label').text

        select2 = select2_div.find('select')
        self.settings = self.__get_settings(soup, select2['data-krajee-select2'])
        self.allow_clear = self.settings['allowClear'] if 'allowClear' in self.settings else False
        self.options = self.__get_options(select2.find_all('option'), self.required, self.allow_clear)

    @staticmethod
    def __get_settings(soup, option_id):
        declaration_start = soup.text.find(f'window.{option_id}')
        setting_start = soup.text.find('{', declaration_start)
        setting_end = soup.text.find('}', setting_start)
        return json.loads(soup.text[setting_start:setting_end + 1])

    @staticmethod
    def __get_options(soup, required, allow_clear):

        def get_name(value, name):
            return '' if valid_empty_value(value) else name

        def get_value(option):
            return option['value']

        def valid_empty_value(value):
            return value == '' and allow_clear and not required

        def valid_value(value):
            return not (value == '' and allow_clear and required)

        return [
            Option(
                get_name(get_value(option), option.text),
                get_value(option)
            )
            for option
            in soup
            if valid_value(get_value(option))
        ]
