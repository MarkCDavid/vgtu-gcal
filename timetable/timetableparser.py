from bs4 import BeautifulSoup
from timetable.timetabletranslator import data_label_translations, dow_translations
from timetable.timetableformatter import TimetableFormatter
from timetable.timetable import Timetable, TimetableWeekday, TimetableEvent


def fetch_language(soup):
    return soup.find("html")["lang"]


def fetch_timetable(soup):
    return soup.find("div", class_="table-container")


def fetch_weekday_table(timetable):
    return timetable.find_all("div", class_="grid-view")


def fetch_table_heading(weekday_table):
    return weekday_table.find("h3", class_="tableheading")


def fetch_table(weekday_table):
    return weekday_table.find("tbody")


def fetch_table_rows(table):
    return table.find_all("tr")


def fetch_table_row_data(table_row):
    return table_row.find_all("td")


def create_soup(path):
    with open(path, "r", encoding="utf-8") as html:
        return BeautifulSoup(html.read(), 'lxml')


def table_iterator(weekday_table):
    table = fetch_table(weekday_table)
    for row in fetch_table_rows(table):
        yield fetch_table_row_data(row)


def parse_weekday_data(weekday_table):
    heading = fetch_table_heading(weekday_table).text
    return [x for x in heading.split(" ") if len(x) > 1]


def parse_event(row, formatter):
    event = TimetableEvent()
    event.Update([formatter.ttformat(data) for data in row])
    return event


def parse_weekday(weekday_table, language, formatter):
    weekday = TimetableWeekday()
    weekday.UpdateData(parse_weekday_data(weekday_table), dow_translations[language])
    for row in table_iterator(weekday_table):
        weekday.AddEvent(parse_event(row, formatter))
    return weekday


def parse_timetable(weekday_tables, language, formatter):
    timetable = Timetable()
    for weekday_table in weekday_tables:
        timetable.AddWeekday(parse_weekday(weekday_table, language, formatter))
    return timetable


def parse(path):
    soup = create_soup(path)
    language = fetch_language(soup)
    formatter = TimetableFormatter(data_label_translations[language])
    weekday_tables = fetch_weekday_table(fetch_timetable(soup))
    return parse_timetable(weekday_tables, language, formatter)
