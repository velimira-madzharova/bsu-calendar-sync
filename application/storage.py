#!/usr/bin/env python3

from pymongo import MongoClient
from google_calendar import Calendar

class Storage:

    def __init__(self):
        client = MongoClient()
        self.db = client.courses
        self.actions = []
        self.calendar = Calendar()

    def save(self, courses):

        saved_graphics = self.__get_graphics()

        for saved_graphic in saved_graphics:
            found = False
            for course_graphic in reversed(courses):
                if saved_graphic['start_date'] == course_graphic['start_date'] and \
                   saved_graphic['end_date'] == course_graphic['end_date'] and \
                   saved_graphic['course_name'] == course_graphic['course_name']:
                    self.__update(saved_graphic, course_graphic)
                    courses.remove(course_graphic)
                    found = True
                    break

            # course has been deleted from online schedule. Therefore we delete it as well.
            if not found:
               self.__delete(saved_graphic)

        for course_graphic in courses:
            self.__insert(course_graphic)

    def get_actions(self):
        return self.actions


    def __action(self, type, graphic, data = []):
        self.actions.append({
          'type': type,
          'graphic': graphic,
          'data': data
        })

    def __get_graphics(self):
        mongo_graphics = self.db.graphic.find({})

        return mongo_graphics

    def __update(self, saved_graphic, course_graphic):
        diff = { key: val for key, val in course_graphic.items() if saved_graphic.get(key, None) != val }
        if diff:
           self.calendar.delete_event(saved_graphic['calendar_id'])
           calendar_desc = course_graphic['course_lecturer'] + ', ' + str(course_graphic['course_location']) + ', ' + str(course_graphic['course_type']) + ', ' + str(course_graphic['educational_form']) + ', ' + str(course_graphic['course_year'])
           calendar_id = self.calendar.insert_event(course_graphic['course_name'], calendar_desc, course_graphic['graphic_url'], course_graphic['start_date'], course_graphic['end_date'])
           if calendar_id:
              course_graphic['calendar_id'] = calendar_id
              self.db.graphic.update_one({'_id' : saved_graphic['_id']}, {'$set': course_graphic})
              self.__action('update', course_graphic, diff)

    def __delete(self, saved_graphic):
        self.calendar.delete_event(saved_graphic['calendar_id'])
        self.db.graphic.delete_one({'_id' : saved_graphic['_id']})
        self.__action('delete', saved_graphic)

    def __insert(self, course_graphic):
        calendar_desc = course_graphic['course_lecturer'] + ', ' + str(course_graphic['course_location']) + ', ' + str(course_graphic['course_type']) + ', ' + str(course_graphic['educational_form']) + ', ' + str(course_graphic['course_year'])

        calendar_id = self.calendar.insert_event(course_graphic['course_name'], calendar_desc, course_graphic['graphic_url'], course_graphic['start_date'], course_graphic['end_date'])
        if calendar_id:
           course_graphic['calendar_id'] = calendar_id
           self.db.graphic.insert_one(course_graphic)
           self.__action('insert', course_graphic)
