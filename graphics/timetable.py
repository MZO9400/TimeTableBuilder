from graphics.Graphics import Graphics


class TimeTable(Graphics):
    def __init__(self, parent, data, window_title="Time Table"):
        super().__init__(parent, window_title)
        self.data = data

    def __init_window__(self):
        pass
