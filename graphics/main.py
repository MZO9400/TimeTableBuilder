class TimeTableBuilder:
    def __init__(self, window, course_alloc, window_title="Time Table Builder"):
        self.window = window
        self.course_alloc = course_alloc
        self.window.title(window_title)
        self.window.mainloop()

        self.sub_window = None
