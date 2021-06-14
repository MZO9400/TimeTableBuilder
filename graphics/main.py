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
