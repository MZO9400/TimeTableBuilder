import tkinter

from graphics.Graphics import Graphics
from helpers.functions import DAYS, get_times

STICKY_ALL = tkinter.N + tkinter.W + tkinter.S + tkinter.E


class TimeTable(Graphics):
    def __init__(self, parent, data, window_title="Time Table"):
        self.data = data
        super().__init__(parent, window_title)

    def __init_window__(self):
        self.labels = {'days': {}, 'times': {}}
        data = self.data()
        times = ["{}:{}".format(time['hours'], time['minutes']) for time in get_times(data)]

        self.first_corner = tkinter.Label(self.window, text="Time Table")
        self.first_corner.grid(row=1, column=1, ipadx=30, ipady=30, sticky=STICKY_ALL)

        for index, day in enumerate(DAYS, start=1):
            self.window.rowconfigure(index - 1, pad=0)
            self.labels['days'][day] = tkinter.Label(
                self.window,
                justify=tkinter.RIGHT,
                text=day.upper(),
                borderwidth=2,
                relief='solid'
            )
            self.labels['days'][day].grid(row=index + 1, column=1, ipadx=30, ipady=30, sticky=STICKY_ALL)

        for index, time in enumerate(times, start=1):
            self.window.columnconfigure(index - 1, pad=0)
            self.labels['times'][time] = tkinter.Label(self.window, text=time, borderwidth=2, relief='solid')
            self.labels['times'][time].grid(row=1, column=index + 1, ipadx=30, ipady=30, sticky=STICKY_ALL)
