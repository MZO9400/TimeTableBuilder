import pyswip

from helpers.functions import str_to_time

prolog = pyswip.Prolog()
prolog.consult('./knowledgebase/course_allocations.pl')


def query(
        room="ROOM",
        day="DAY",
        section="SECTION",
        course="COURSE",
        instructor="INSTRUCTOR",
        time="TIME"
):
    query_string = 'course_allocation({section}, {course}, {instructor}, {time}, {day}, {room})' \
        .format(course=course, section=section, instructor=instructor, time=time, day=day, room=room)
    return prolog.query(query_string)


# Q1, Q2
def schedule(class_name, day="DAY"):
    return query(room=class_name, day=day)


# Q3
def time_slots(class_name):
    return list(
        set(
            [
                {'TIME': str_to_time(r['TIME']), 'DAY': r['DAY']}
                for r in query(room=class_name)
            ]
        )
    )
