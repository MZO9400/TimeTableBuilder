import tkinter


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
            self.window.mainloop()

    class AddNewRule:
        def __init__(self, parent):
            self.window = tkinter.Tk()
            self.parent = parent

            self.window.title('Add Data')
            self.window.mainloop()

    def delete_sub_window(self):
        if self.sub_window is not None:
            self.sub_window.window.destroy()
            self.sub_window = None

    def create_time_table(self):
        self.sub_window = self.TimeTable(self, self.get_time_table_data)

    def create_add_new_rule(self):
        self.sub_window = self.AddNewRule(self)

    def get_time_table_data(self):
        pass

