import tkinter
import tkinter.messagebox

from helpers.functions import time_input_to_str


class AddNewRule:
    def __init__(self, parent, add_data):
        self.window = tkinter.Tk()
        self.parent = parent
        self.add_data = add_data

        self.window.title('Add Data')
        self.window.protocol("WM_DELETE_WINDOW", self.parent.delete_sub_window)

        self.data_list = ('room', 'day', 'section', 'course', 'instructor', 'time')

        self.__init_window__()

    def start(self):
        self.window.mainloop()

    def __init_window__(self):
        self.window.columnconfigure(0, pad=6)
        self.window.columnconfigure(1, pad=9)

        self.window.rowconfigure(0, pad=3)
        self.window.rowconfigure(1, pad=3)
        self.window.rowconfigure(2, pad=3)
        self.window.rowconfigure(3, pad=3)
        self.window.rowconfigure(4, pad=3)
        self.window.rowconfigure(5, pad=3)
        self.window.rowconfigure(6, pad=3)

        self.labels = {}
        self.strings = {}
        self.entries = {}
        for index, label in enumerate(self.data_list):
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
        self.insert_button.grid(row=7, column=1, columnspan=3)

    def save_data(self):
        data = {}
        try:
            for index, label in enumerate(self.data_list):
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
                    data[label] = self.entries[label].get()
            return data
        except Exception as e:
            tkinter.messagebox.showerror(e.args[0], e.args[1])

