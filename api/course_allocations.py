import pyswip
import os.path
from helpers.functions import str_to_time


class PrologWrapper:
    def __init__(self, filename):
        self.__pl__ = pyswip.Prolog()
        if os.path.isfile(filename):
            self.file = filename
        self.reconsult()

    def reconsult(self):
        try:
            self.__pl__.consult(self.file)
            return True
        except:
            return False

    def query(
            self,
            room="ROOM",
            day="DAY",
            section="SECTION",
            course="COURSE",
            instructor="INSTRUCTOR",
            time="TIME"
    ):
        query_string = 'course_allocation({section}, {course}, {instructor}, {time}, {day}, {room})' \
            .format(course=course, section=section, instructor=instructor, time=time, day=day, room=room)
        return self.__pl__.query(query_string)

    def insert(self, room, day, section, course, instructor, time):
        try:
            fact = "\ncourse_allocation({section}, {course}, {instructor}, {time}, {day}, {room}).\n"
            with open(self.file, 'a+') as kb:
                kb.write(
                    fact.format(
                        section=section.lower().replace(' ', '_'),
                        course=course.lower().replace(' ', '_'),
                        instructor=instructor.lower().replace(' ', '_'),
                        time=time,
                        day=day.lower(),
                        room=room.lower()
                    )
                )
            return self.reconsult()
        except IOError:
            return -1

    # Q1, Q2
    def schedule(self, class_name, day="DAY"):
        return self.query(room=class_name, day=day)

    # Q3
    def time_slots(self, class_name):
        return [
            {'TIME': str_to_time(r['TIME']), 'DAY': r['DAY']}
            for r in self.query(room=class_name)
        ]

    # Q4
    def instructors(self, class_name):
        return list(
            set(
                [
                    r['INSTRUCTOR']
                    for r in self.query(room=class_name)
                ]
            )
        )
