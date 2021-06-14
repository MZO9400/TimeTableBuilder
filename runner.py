from tkinter import Tk

from api.course_allocations import PrologWrapper
from graphics.main import TimeTableBuilder

KNOWLEDGEBASE = "knowledgebase/course_allocations.pl"

tt = TimeTableBuilder(
    window=Tk(),
    course_alloc=PrologWrapper(KNOWLEDGEBASE)
).start()
