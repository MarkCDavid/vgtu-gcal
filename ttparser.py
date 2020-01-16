from bs4 import BeautifulSoup
from tttranslator import data_title_translations
from ttformatter import TTFormatter
import tt

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

def parse(path):
    soup = create_soup(path)
    language = fetch_language(soup)
    translation = data_title_translations[language]
    ttf = TTFormatter(translation)
    timetable = fetch_timetable(soup)
    weekday_tables = fetch_weekday_table(timetable)
    timetable = tt.TimeTable()
    for weekday_table in weekday_tables:
        ttweekday = tt.TimeTableWeekday()
        heading = fetch_table_heading(weekday_table).text
        weekday_data = [x for x in heading.split(" ") if len(x) > 1]
        ttweekday.UpdateData(weekday_data)
        for weekday_row in table_iterator(weekday_table):
            ttevent = tt.TimeTableEvent()
            ttevent_data = []
            for weekday_data in weekday_row:
                ttevent_data.append(ttf.ttformat(weekday_data))
            ttevent.Update(ttevent_data)
            ttweekday.AddEvent(ttevent)
        timetable.AddWeekday(ttweekday)
    return timetable
