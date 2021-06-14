import tkinter
from abc import ABCMeta, abstractmethod


class Graphics(metaclass=ABCMeta):
    def __init__(self, parent, window_title):
        self.window = tkinter.Tk()
        self.parent = parent

        self.window.title(window_title)
        if callable(parent.delete_sub_window):
            self.window.protocol("WM_DELETE_WINDOW", self.parent.delete_sub_window)

        self.__init_window__()

    def start(self):
        self.window.mainloop()

    @abstractmethod
    def __init_window__(self):
        pass
