from api.course_allocations import PrologWrapper
from graphics import TimeTableBuilder

KNOWLEDGEBASE = "knowledgebase/course_allocations.pl"

TimeTableBuilder(course_alloc=PrologWrapper(KNOWLEDGEBASE)).start()
