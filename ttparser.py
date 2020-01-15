from bs4 import BeautifulSoup
from ttformatter import ttformat


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
        for data in fetch_table_row_data(row):
            yield data


def parse(path):
    soup = create_soup(path)
    #timetable = fetch_timetable(soup)
    #weekday_tables = fetch_weekday_table(timetable)
    # for weekday_table in weekday_tables:
    for data in table_iterator(soup):
        ttformat(data)
    #break
