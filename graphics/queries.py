import tkinter
import tkinter.messagebox

from api.course_allocations import PrologWrapper
from graphics import Graphics
from helpers.functions import query_builder, prettify_query


class Queries(Graphics):
    """
    Query runner class, uses functions::query_builder function to fetch queries
    """
    def __init__(self, parent, course_allocator, window_title="Queries"):
        if not isinstance(course_allocator, PrologWrapper):
            raise "Course allocator is invalid"

        self.queries = query_builder(course_allocator)
        self.dropdown = None
        self.dropdown_variable = None
        self.output = None
        self.output_variable = None
        self.query_index = None
        self.inputs = []

        super().__init__(parent=parent, window_title=window_title)

    def __init_window__(self):
        self.window.rowconfigure(0, pad=10)
        self.window.columnconfigure(0, pad=10)
        self.window.columnconfigure(1, pad=10)

        # Create a dropdown with queries from functions::query_builder
        self.dropdown_variable = tkinter.StringVar(self.window, value="Select a Query", name="Query Selector")
        self.dropdown = tkinter.OptionMenu(self.window,
                                           self.dropdown_variable,
                                           *map(lambda val: val['text'], self.queries),
                                           command=self.create_query)
        self.dropdown.grid(row=1, column=1)

        self.button_run = tkinter.Button(self.window, text="Run Query", command=self.run_query)

    def create_query(self, query):
        """
        Creates dynamic labels and entries for queries and maps them on grid
        :param query: Query is selected option from the dropdown
        :return: None
        """
        if self.button_run.grid_info() == {}:
            self.button_run.grid(row=1, column=2)
        else:
            self.destroy_inputs()

        # Fetch data from functions::query_builder and save index to query_index,
        # map each value for query_builder()[iterator]::inputs to window
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
            # Save each value to self.inputs for destroying later on
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
        """
        Run query saved in query_builder()[iter]::query lambda, map output to a tkinter.messagebox.showinfo
        :return: None
        """
        data = list(map(lambda value: value['entry'].get().lower(), self.inputs))
        if self.validate_data(data):
            if '' in data:
                data.remove('')
            data_generator = self.queries[self.query_index]['query'](*data)  # call the lambda
            output = prettify_query(list(data_generator))
            tkinter.messagebox.showinfo("Output", output)
        else:
            tkinter.messagebox.showerror("Missing fields", "Please fill all required fields")

    def destroy_inputs(self):
        """
        boom, self-explanatory
        :return: None
        """
        for inp in self.inputs:
            for key, obj in inp.items():
                if not isinstance(obj, tkinter.StringVar):  # StringVar cannot be .destroy()-ed
                    obj.destroy()
                del obj
        self.inputs = []

    def validate_data(self, data):
        """
        Makes sure required fields are filled
        :param data: list of strings corresponding to query_builder()[iter]::inputs
        :return:
        """
        for index, datum in enumerate(data):
            if datum == '' and self.queries[self.query_index]['inputs'][index]['required'] is True:
                return False
        return True
