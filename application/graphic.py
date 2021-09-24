#!/usr/bin/env python3
import requests
import re
from bs4 import BeautifulSoup
import datetime as d
import itertools
from urllib.parse import urlencode

class Graphic:

    base_url = "https://e-services.bfu.bg/common/"
    graphics_path = "graphic.php"
    week_date_regex = r"\d{2}.\d{2}.\d{4}"
    graphic_date_regex = r"\d{2}.\d{2}\s\d{2}"
    graphic_distance_learning_regex = r"graphic_view"
    today = d.datetime.today()
#      + d.timedelta(days=14)

    def __init__(self, courses):
        self.courses_list = courses['all']

    def weeks(self, centre, educational_form, course_year):
        query = urlencode({'c': centre, 'o': educational_form, 'k': course_year})
        full_url = self.base_url + self.graphics_path + "?" + query

        r = requests.get(url = full_url)
        soup = BeautifulSoup(r.text, 'html.parser')

        weeks_graphic_urls = []
        for link in soup.find_all(href=re.compile('graphic')):
            week_dates = re.findall(self.week_date_regex, link.string)
#             if len(week_dates) != 2:
#                continue

            week_from = d.datetime.strptime(week_dates[0], '%d.%m.%Y')
            week_to = d.datetime.strptime(week_dates[1], '%d.%m.%Y')
            week_to = week_to + d.timedelta(days=1)

#             if week_from > self.today - d.timedelta(days=7) and week_from <= self.today + d.timedelta(days=7):
            weeks_graphic_urls.append({
            'href': link.get('href'),
            'week_from': week_from,
            'week_to': week_to,
            'year': week_from.year,
            'educational_form': educational_form,
            'course_year': course_year})
        return weeks_graphic_urls

    def courses(self, week):
        full_url = self.base_url + week['href']

        r = requests.get(url = full_url)
        soup = BeautifulSoup(r.text, 'html.parser')

        cells = soup.find('table').find_all('td', class_='info')
        courses_raw = []
        for cell in cells:
            for course in self.courses_list:
                if course in cell:
                   start_date_list = re.findall(self.graphic_date_regex, str(cell.parent.contents[1]))
                   start_date = d.datetime.strptime(start_date_list[0] + str(week['year']), '%d.%m %H%Y')
                   end_date = start_date + d.timedelta(hours = int(cell['rowspan']))

                   courses_raw.append({
                       "start_date": start_date,
                       "end_date": end_date,
                       "educational_form": week['educational_form'],
                       "course_year": week['course_year'],
                       "course_name": cell.contents[0],
                       "course_lecturer" : cell.contents[2],
                       "course_location" : cell.contents[4] if len(cell.contents) >= 4 else False,
                       "course_type" : cell.contents[6] if len(cell.contents) >= 6 else False,
                       "graphic_url" : full_url})

        courses = list(courses_raw for courses_raw,_ in itertools.groupby(courses_raw))

        return courses

    def distance_learning_weeks(self, centre, educational_form, course_year):
        query = urlencode({'c': centre, 'o': educational_form, 'k': course_year})
        full_url = self.base_url + self.graphics_path + "?" + query

        r = requests.get(url = full_url)
        soup = BeautifulSoup(r.text, 'html.parser')

        weeks_graphic_urls = []
        for link in soup.find_all(href=re.compile('graphic')):
            weeks_graphic_urls.append({
            'href': link.get('href'),
            'week_from': '',
            'week_to': '',
            'year': '',
            'educational_form': educational_form,
            'course_year': course_year})
        return weeks_graphic_urls

    def distance_learning_courses(self, week):
        full_url = self.base_url + week['href']

        r = requests.get(url = full_url)
        soup = BeautifulSoup(r.text, 'html.parser')

        cells = soup.find('table').find_all('td')
        courses_raw = []

        table_rows = soup.find('table').find_all('tr')
        week['week_from'] = d.datetime.strptime(table_rows[1].contents[1].get_text(), '%d.%m.%Y')
        week['week_to'] = d.datetime.strptime(table_rows[len(table_rows) - 1].contents[1].get_text(), '%d.%m.%Y')
        week['year'] = week['week_to'].year

        for cell in cells:
            for course in self.courses_list:
                # cell: ['\n', <td>04.10.2021</td>, '\n', <td>15-18</td>, '\n', <td>106</td>, '\n', <td align="left">лекции</td>, '\n', <td align="left">Физика и материалознание</td>, '\n', <td align="left">доц.д-р Лецковска</td>, '\n', <td>-</td>, '\n']
                if course in cell:
                    # cell.parent.contents[1]
                    start_date_list = cell.parent.contents[1].get_text()
                    start_time_list = cell.parent.contents[3].get_text()
                    course_time = start_time_list.split('-')
                    start_date = d.datetime.strptime(start_date_list + course_time[0], '%d.%m.%Y%H')
                    end_date = d.datetime.strptime(start_date_list + course_time[1], '%d.%m.%Y%H')

                    courses_raw.append({
                       "start_date": start_date,
                       "end_date": end_date,
                       "educational_form": week['educational_form'],
                       "course_year": week['course_year'],
                       "course_name": cell.parent.contents[9].get_text(),
                       "course_lecturer" : cell.parent.contents[11].get_text(),
                       "course_location" : cell.parent.contents[5].get_text(),
                       "course_type" : cell.parent.contents[7].get_text(),
                       "graphic_url" : full_url})

        courses = list(courses_raw for courses_raw,_ in itertools.groupby(courses_raw))

        return {'courses': courses, 'week': week}