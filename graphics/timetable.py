import tkinter

from graphics.Graphics import Graphics
from helpers.functions import DAYS, get_times, str_to_time

STICKY_ALL = tkinter.N + tkinter.W + tkinter.S + tkinter.E
IPAD = 30
PAD = 0


class TimeTable(Graphics):
    """
    Maps knowledgebase to python grid
    """
    def __init__(self, parent, data, window_title="Time Table"):
        """

        :param parent: parent window
        :param data: callback to fetch data from knowledgebase
        :param window_title: Title
        """
        self.data = data
        super().__init__(parent, window_title)

    def __init_window__(self):
        """
        Timetable is a bunch of labels,
        Labels are of three types:
            days,
            times,
            classes
        :return: None
        """
        self.labels = {'days': {}, 'times': {}, 'classes': {}}
        data = list(self.data())

        classes = set(map(lambda cl: cl['SECTION'].upper().replace('_', ' '), data))

        # Dropdown with class/section name
        self.drop_down_var = tkinter.StringVar(self.window)
        self.drop_down_var.set("CLASS")
        self.drop_down = tkinter.OptionMenu(self.window, self.drop_down_var, *classes, command=self.on_class_change)
        self.drop_down.grid(row=1, column=1, ipadx=IPAD, ipady=IPAD, sticky=STICKY_ALL)

    def destroy_all(self):
        """
        Destroy all elements
        :return: boolean
        """
        try:
            labels_types = self.labels
            for label_type in list(labels_types):
                labels = list(self.labels[label_type])
                for label in labels:
                    self.labels[label_type][label].destroy()
                    del self.labels[label_type][label]
            return True
        except:
            return False

    def on_class_change(self, selected_option):
        """
        Destroys and remaps new timetable with its data
        :param selected_option: String for selected class/section
        :return: None
        """
        data = list(self.data(selected_option.lower().replace(' ', '_')))
        time_list = get_times(data)
        times = [
            "{}:{}-{}:{}".format(
                time_list[idx]['hours'], time_list[idx]['minutes'],
                time_list[idx + 1]['hours'], time_list[idx + 1]['minutes']
            )
            for idx in range(len(time_list) - 1)
        ]

        self.destroy_all()
        for index, day in enumerate(DAYS, start=1):
            self.window.rowconfigure(index - 1, pad=PAD)
            self.labels['days'][day] = tkinter.Label(
                self.window,
                justify=tkinter.RIGHT,
                text=day.upper(),
                borderwidth=2,
                relief='solid'
            )
            self.labels['days'][day].grid(row=index + 1, column=1, ipadx=IPAD, ipady=IPAD, sticky=STICKY_ALL)

        for index, time in enumerate(times, start=1):
            self.window.columnconfigure(index - 1, pad=PAD)
            self.labels['times'][time] = tkinter.Label(self.window, text=time, borderwidth=2, relief='solid')
            self.labels['times'][time].grid(row=1, column=index + 1, ipadx=IPAD, ipady=IPAD, sticky=STICKY_ALL)

        for index, entry in enumerate(data):
            grid_info = self.get_grid_info(entry)
            entry_index = str(entry)
            self.labels['classes'][entry_index] = tkinter.Label(
                self.window,
                text="{}\n{}\n{}".format(
                    entry['COURSE'].upper().replace('_', ' '),
                    entry['INSTRUCTOR'].upper().replace('_', ' '),
                    entry['ROOM'].upper().replace('_', ' '),
                ),
                borderwidth=2,
                relief='solid'
            )
            self.labels['classes'][entry_index].grid(
                row=grid_info['row'],
                rowspan=grid_info['rowspan'],
                column=grid_info['column'],
                columnspan=grid_info['columnspan'],
                sticky=STICKY_ALL
            )

    def get_grid_info(self, data):
        """
        Calculates the position of an element in grid given the day and time
        :param data: A prolog query response element
        :return: Grid info considering element location
        """
        grid_info = {}
        row = self.labels['days'][data['DAY']].grid_info()
        grid_info['row'] = row['row']
        grid_info['rowspan'] = row['rowspan']

        time = str_to_time(data['TIME'])
        time_start = "{}:{}".format(time['start']['hours'], time['start']['minutes'])
        time_end = "{}:{}".format(time['end']['hours'], time['end']['minutes'])

        times = list(self.labels['times'].keys())

        time_start = [i for i in times if i.startswith(time_start)][0]
        time_end = [i for i in times if i.endswith(time_end)][0]

        col_start = self.labels['times'][time_start].grid_info()
        col_end = self.labels['times'][time_end].grid_info()

        grid_info['column'] = col_start['column']
        grid_info['columnspan'] = col_end['column'] - col_start['column'] + 1

        return grid_info
