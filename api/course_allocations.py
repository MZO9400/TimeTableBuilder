import pyswip

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
