import tkinter

from graphics.timetable import TimeTable
from graphics.addnewrule import AddNewRule
from helpers.functions import verify_time


class TimeTableBuilder:
    def __init__(self, window, course_alloc, window_title="Time Table Builder"):
        self.window = window
        self.course_alloc = course_alloc
        self.window.title(window_title)

        self.sub_window = None
        self.button_show_time_table = None
        self.button_add_new_rule = None

        self.TimeTable = TimeTable
        self.AddNewRule = AddNewRule

        self.__init_window__()

        self.window.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.window.mainloop()

    def __init_window__(self):
        self.window.columnconfigure(0, pad=3)
        self.window.columnconfigure(1, pad=3)

        self.window.rowconfigure(0, pad=3)

        self.button_show_time_table = tkinter.Button(
            self.window,
            text="Display Time Table",
            width=50,
            command=self.create_time_table)
        self.button_show_time_table.grid(row=1, column=1)

        self.button_add_new_rule = tkinter.Button(
            self.window,
            text="Add new data",
            width=50,
            command=self.create_time_table)
        self.button_add_new_rule.grid(row=1, column=2)

    def on_exit(self):
        self.delete_sub_window()
        self.window.destroy()

    def delete_sub_window(self):
        if self.sub_window is not None:
            self.sub_window.window.destroy()
            self.sub_window = None

    def create_time_table(self):
        self.delete_sub_window()
        self.sub_window = self.TimeTable(self, self.get_time_table_data)
        self.sub_window.start()

    def create_add_new_rule(self):
        self.delete_sub_window()
        self.sub_window = self.AddNewRule(self, self.add_new_rule)
        self.sub_window.start()

    def get_time_table_data(self):
        return self.course_alloc.query()

    def add_new_rule(self, room, day, section, course, instructor, time):
        if verify_time(room, day, section, course, instructor, time):
            self.course_alloc.insert(room, day, section, course, instructor, time)
