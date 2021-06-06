import pyswip

prolog = pyswip.Prolog()
prolog.consult('./knowledgebase.pl')


def fetch(
        room="ROOM",
        day="DAY",
        section="SECTION",
        course="COURSE",
        instructor="INSTRUCTOR",
        time="TIME"
):
    query = 'course_allocation({section}, {course}, {instructor}, {time}, {day}, {room})' \
        .format(course=course, section=section, instructor=instructor, time=time, day=day, room=room)
    return prolog.query(query)
