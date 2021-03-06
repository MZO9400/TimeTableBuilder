import tkinter
from abc import ABCMeta, abstractmethod


class Graphics(metaclass=ABCMeta):
    """
    Generic base class for sub-windows
    """

    def __init__(self, parent=None, window_title="Window"):
        self.window = tkinter.Tk()
        self.parent = parent

        self.window.title(window_title)
        if parent is not None and parent.delete_sub_window is not None and callable(parent.delete_sub_window):
            self.window.protocol("WM_DELETE_WINDOW", self.parent.delete_sub_window)

        self.__init_window__()

    def start(self):
        """
        API to run main loop
        :return: self
        """
        self.window.mainloop()
        return self

    @abstractmethod
    def __init_window__(self):
        """
        Abstract method, uncallable
        :return: None
        """
        pass
