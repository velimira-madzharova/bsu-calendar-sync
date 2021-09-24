#!/usr/bin/env python3

import itertools
from config import Config
from graphic import Graphic
from storage import Storage

def main():

    config = Config()
    storage = Storage()
    graphic = Graphic(config.get("courses"))
    graphic_cfg = config.get("graphic")
    all_params = get_graphic_params(graphic_cfg)
    courses = list()
    seen_courses = list()

    for params in all_params:
        if params[1] == 1:
            weeks = graphic.weeks(params[0], params[1], params[2])

            for week in weeks:
                new_courses = graphic.courses(week)
                for new_course in new_courses:
                    check_new_course = new_course['start_date'].strftime("%d%m%Y%H") + '-' + new_course['end_date'].strftime("%d%m%Y%H") + '-' +  new_course['course_name']
                    if check_new_course not in seen_courses:
                        seen_courses.append(check_new_course)
                        courses.append(new_course)
        else:
            distance_learning_weeks = graphic.distance_learning_weeks(params[0], params[1], params[2])

            for week in distance_learning_weeks:
                new_courses = graphic.distance_learning_courses(week)
                for new_course in new_courses['courses']:
                    check_new_course = new_course['start_date'].strftime("%d%m%Y%H") + '-' + new_course['end_date'].strftime("%d%m%Y%H") + '-' +  new_course['course_name']
                    if check_new_course not in seen_courses:
                        seen_courses.append(check_new_course)
                        courses.append(new_course)

    storage.save(courses)
    print_actions(storage.get_actions())
    print('Calendar sync finished.')

def print_actions(actions):
    for action in actions:
        if action['type'] == 'insert':
           print(f"\033[92mEvent Inserted\033[0m")
           print(action['graphic']['course_name'] + ' ' + action['graphic']['start_date'].strftime("%Y/%m/%d, %H:%M") + ' - ' + action['graphic']['end_date'].strftime("%Y/%m/%d, %H:%M"))
        if action['type'] == 'update':
           print(f"\033[94mEvent Updated\033[0m")
           print(action['graphic']['course_name'] + ' ' + action['graphic']['start_date'].strftime("%Y/%m/%d, %H:%M") + ' - ' + action['graphic']['end_date'].strftime("%Y/%m/%d, %H:%M"))
        if action['type'] == 'delete':
           print(f"\033[93mEvent Deleted\033[0m")
           print(action['graphic']['course_name'] + ' ' + action['graphic']['start_date'].strftime("%Y/%m/%d, %H:%M") + ' - ' + action['graphic']['end_date'].strftime("%Y/%m/%d, %H:%M"))

        print()

def get_graphic_params(config):
    config_params = [config["centre"], config["educational_form"], config["course_year"]]
    return list(itertools.product(*config_params))

if __name__ == "__main__":
    main()