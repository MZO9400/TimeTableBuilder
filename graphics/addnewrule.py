import tkinter
import tkinter.messagebox
from tkinter import simpledialog

from graphics.Graphics import Graphics
from helpers.functions import time_input_to_str, DATA_LIST, check_time_clash, str_to_time


class AddNewRule(Graphics):
    """
    Add New Rule class
    Adds an entry in timetable knowledgebase
    """

    def __init__(self, parent, add_data, window_title="Add Data"):
        self.add_data = add_data
        super().__init__(parent, window_title)

    def __init_window__(self):
        """
        Maps entries from DATA_LIST to GUI,
        elements are accessible through:
        self.labels for labels,
        self.strings for stringvars,
        self.entries for entries
        :return: None
        """
        self.window.columnconfigure(0, pad=10)
        self.window.columnconfigure(1, pad=20)

        self.window.rowconfigure(0, pad=3)
        self.window.rowconfigure(1, pad=3)
        self.window.rowconfigure(2, pad=3)
        self.window.rowconfigure(3, pad=3)
        self.window.rowconfigure(4, pad=3)
        self.window.rowconfigure(5, pad=3)
        self.window.rowconfigure(6, pad=15)

        self.labels = {}
        self.strings = {}
        self.entries = {}
        for index, label in enumerate(DATA_LIST):
            self.labels[label] = tkinter.Label(
                self.window,
                justify=tkinter.RIGHT,
                text=label.upper(),
                anchor=tkinter.W
            )
            self.labels[label].grid(sticky=tkinter.W, row=index, column=1)

            self.strings[label] = tkinter.StringVar(self.window)

            self.entries[label] = tkinter.Entry(self.window, textvariable=self.strings[label])
            self.entries[label].grid(sticky=tkinter.W, row=index, column=2)

        self.insert_button = tkinter.Button(self.window, command=self.save_data, text='INSERT')
        self.insert_button.grid(row=7, column=0, columnspan=2)

        self.insert_raw = tkinter.Button(self.window, command=self.popup_raw_insert, text='RAW QUERY')
        self.insert_raw.grid(row=7, column=2, columnspan=2)

    def popup_raw_insert(self):
        inp = simpledialog.askstring(title="RAW", prompt="Please insert your rule/fact:")
        if inp:
            if self.parent.course_alloc.is_query_valid("{}".format(inp)):
                self.parent.course_alloc.insert_raw(inp + '.')

    def save_data(self):
        """
        Takes input from entries, checks for errors, and then adds to knowledgebase
        :return: None
        """
        data = {}
        try:
            for index, label in enumerate(DATA_LIST):
                entry_input = self.entries[label].get()
                if entry_input == '':
                    raise Exception("{} is empty".format(label), "Please fill all fields")
                if label == 'time':
                    time = time_input_to_str(entry_input)
                    if not time:
                        raise Exception("Time is malformed", "Example: 9:30-13:30")
                    else:
                        data[label] = time
                else:
                    data[label] = self.entries[label].get().lower().replace(' ', '_')
            knowledgebase = list(self.parent.get_time_table_data())
            # filter clashes by time and day
            clashes = [
                val
                for val in knowledgebase
                if check_time_clash(str_to_time(data['time']), str_to_time(val['TIME'])) and data['day'] == val['DAY']
            ]
            # filter by whether instructor, room, or class is busy
            clashes = [
                val
                for val in clashes
                if data['instructor'] == val['INSTRUCTOR'] or
                   data['room'] == val['ROOM'] or
                   data['section'] == val['SECTION']
            ]
            if len(clashes) > 0:
                raise Exception("Clash occurred", "Please consult time table for more details")
            self.parent.course_alloc.insert(
                data['room'],
                data['day'],
                data['section'],
                data['course'],
                data['instructor'],
                data['time']
            )
        except Exception as e:
            tkinter.messagebox.showerror(e.args[0], e.args[1])
