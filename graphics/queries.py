import tkinter
import tkinter.messagebox

from graphics.Graphics import Graphics
from helpers.functions import query_builder, prettify_query


class Queries(Graphics):
    def __init__(self, parent):
        self.dropdown = None
        self.dropdown_variable = None
        self.output = None
        self.output_variable = None
        self.query_index = None

        self.queries = query_builder(parent.course_alloc)

        self.inputs = []

        super().__init__(parent=parent)

    def __init_window__(self):
        self.window.rowconfigure(0, pad=10)
        self.window.columnconfigure(0, pad=10)
        self.window.columnconfigure(1, pad=10)

        self.dropdown_variable = tkinter.StringVar(self.window, value="Select a Query", name="Query Selector")
        self.dropdown = tkinter.OptionMenu(self.window,
                                           self.dropdown_variable,
                                           *map(lambda val: val['text'], self.queries),
                                           command=self.create_query)
        self.dropdown.grid(row=1, column=1)

        self.button_run = tkinter.Button(self.window, text="Run Query", command=self.run_query)

    def create_query(self, query):
        if self.button_run.grid_info() == {}:
            self.button_run.grid(row=1, column=2)
        else:
            self.destroy_inputs()

        self.query_index = list(map(lambda val: val['text'], self.queries)).index(query)
        inputs = self.queries[self.query_index]['inputs']
        for index, _input in enumerate(inputs, start=2):
            label = tkinter.Label(
                self.window,
                justify=tkinter.RIGHT,
                text="{}{}".format(_input['name'].upper(), '*' if _input['required'] else ''),
                anchor=tkinter.W
            )
            var = tkinter.StringVar(self.window, name=_input['name'])
            inp = tkinter.Entry(self.window, textvariable=var)
            self.inputs += [
                {
                    'label': label,
                    'entry': inp,
                    'variable': var
                }
            ]
            self.window.rowconfigure(index, pad=10)
            label.grid(row=index, column=1, sticky=tkinter.W)
            inp.grid(row=index, column=2)

    def run_query(self):
        data = list(map(lambda value: value['entry'].get(), self.inputs))
        if self.validate_data(data):
            data_generator = self.queries[self.query_index]['query'](
                *map(lambda val: val if val != '' else None, data)
            )
            output = prettify_query(list(data_generator))
            if output:
                tkinter.messagebox.showinfo("Output", output)
            else:
                tkinter.messagebox.showerror("Unknown error occurred", "Could not show output at this time")
        else:
            tkinter.messagebox.showerror("Missing fields", "Please fill all required fields")

    def destroy_inputs(self):
        for inp in self.inputs:
            for key, obj in inp.items():
                if not isinstance(obj, tkinter.StringVar):
                    obj.destroy()
                del obj
        self.inputs = []

    def validate_data(self, data):
        for index, datum in enumerate(data):
            if datum == '' and self.queries[self.query_index]['inputs'][index]['required'] is True:
                return False
        return True
