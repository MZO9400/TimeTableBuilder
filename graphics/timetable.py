import tkinter


class TimeTable:
    def __init__(self, parent, data):
        self.window = tkinter.Tk()
        self.parent = parent
        self.data = data()

        self.window.title('Time Table')
        self.window.protocol("WM_DELETE_WINDOW", self.parent.delete_sub_window)

    def start(self):
        self.window.mainloop()
