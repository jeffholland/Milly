from widget import Widget

class Number(Widget):
    def __init__(self, master, data, index):
        Widget.__init__(
            self,
            master,
            data,
            index
        )