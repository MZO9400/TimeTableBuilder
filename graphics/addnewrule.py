import tkinter


class AddNewRule:
    def __init__(self, parent, add_data):
        self.window = tkinter.Tk()
        self.parent = parent
        self.add_data = add_data

        self.window.title('Add Data')
        self.window.protocol("WM_DELETE_WINDOW", self.parent.delete_sub_window)

    def start(self):
        self.window.mainloop()
