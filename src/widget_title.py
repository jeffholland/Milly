from widget import Widget

class Title(Widget):
    def __init__(self, master, width, height):

        Widget.__init__(
            self, 
            master, 
            width=width, 
            height=height
        )
        self.widget_config()

    def widget_config(self):
        self.title_label.configure(text="Title")