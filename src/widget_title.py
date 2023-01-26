from widget import Widget

class Title(Widget):
    def __init__(self, master, width, height, font):

        Widget.__init__(
            self, 
            master, 
            width=width, 
            height=height
        )

        self.font = font.copy()
        self.font.configure(size=20)

        self.widget_config()

    def widget_config(self):
        self.title_label.configure(
            text="Title",
            font=self.font
        )