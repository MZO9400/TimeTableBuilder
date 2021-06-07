import pyswip

from helpers.functions import str_to_time


def consult():
    try:
        global prolog
        prolog.consult('./knowledgebase/course_allocations.pl')
        return True
    except:
        return False


prolog = pyswip.Prolog()
consult()


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


def insert(room, day, section, course, instructor, time):
    try:
        fact = "\ncourse_allocation({section}, {course}, {instructor}, {time}, {day}, {room}).\n"
        with open('./knowledgebase/course_allocations.pl', 'a+') as kb:
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
        return consult()
    except IOError:
        return -1


# Q1, Q2
def schedule(class_name, day="DAY"):
    return query(room=class_name, day=day)


# Q3
def time_slots(class_name):
    return [
        {'TIME': str_to_time(r['TIME']), 'DAY': r['DAY']}
        for r in query(room=class_name)
    ]


# Q4
def instructors(class_name):
    return list(
        set(
            [
                r['INSTRUCTOR']
                for r in query(room=class_name)
            ]
        )
    )
