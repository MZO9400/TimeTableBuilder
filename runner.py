from graphics.main import TimeTableBuilder
from api.course_allocations import PrologWrapper
from tkinter import Tk

KNOWLEDGEBASE = "knowledgebase/course_allocations.pl"

tt = TimeTableBuilder(
    window=Tk(),
    course_alloc=PrologWrapper(KNOWLEDGEBASE)
).start()
