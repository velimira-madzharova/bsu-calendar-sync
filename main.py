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
    config_params = [graphic_cfg["centre"], graphic_cfg["educational_form"], graphic_cfg["course_year"]]
    all_params = list(itertools.product(*config_params))

    for params in all_params:
        weeks = graphic.weeks(params[0], params[1], params[2])

        for week in weeks:
            courses = graphic.courses(week)
            storage.save(courses, week)

    for action in storage.get_actions():
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

if __name__ == "__main__":
    main()