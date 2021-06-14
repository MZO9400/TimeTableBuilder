import tkinter

from helpers.functions import verify_time


class TimeTableBuilder:
    def __init__(self, window, course_alloc, window_title="Time Table Builder"):
        self.window = window
        self.course_alloc = course_alloc
        self.window.title(window_title)
        self.window.mainloop()

        self.sub_window = None

    class TimeTable:
        def __init__(self, parent, data):
            self.window = tkinter.Tk()
            self.parent = parent
            self.data = data()

            self.window.title('Time Table')
            self.window.protocol("WM_DELETE_WINDOW", self.parent.delete_sub_window)

        def start(self):
            self.window.mainloop()

    class AddNewRule:
        def __init__(self, parent, add_data):
            self.window = tkinter.Tk()
            self.parent = parent
            self.add_data = add_data

            self.window.title('Add Data')
            self.window.protocol("WM_DELETE_WINDOW", self.parent.delete_sub_window)

        def start(self):
            self.window.mainloop()

    def on_exit(self):
        self.delete_sub_window()
        self.window.destroy()

    def delete_sub_window(self):
        if self.sub_window is not None:
            self.sub_window.window.destroy()
            self.sub_window = None

    def create_time_table(self):
        self.sub_window = self.TimeTable(self, self.get_time_table_data)
        self.sub_window.start()

    def create_add_new_rule(self):
        self.sub_window = self.AddNewRule(self, self.add_new_rule)
        self.sub_window.start()

    def get_time_table_data(self):
        pass

    def add_new_rule(self, room, day, section, course, instructor, time):
        if verify_time(room, day, section, course, instructor, time):
            self.course_alloc.insert(room, day, section, course, instructor, time)
