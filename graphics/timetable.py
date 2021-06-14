import tkinter

from graphics.Graphics import Graphics

STICKY_ALL = tkinter.N + tkinter.W + tkinter.S + tkinter.E


class TimeTable(Graphics):
    def __init__(self, parent, data, window_title="Time Table"):
        self.data = data
        super().__init__(parent, window_title)
        self.data = data

    def __init_window__(self):
        pass
