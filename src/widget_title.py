from widget import Widget

class Title(Widget):
    def __init__(self, master, title, width, height, font):

        Widget.__init__(
            self, 
            master, 
            width=width, 
            height=height
        )

        self.title = title
        self.type = "Title"

        self.font = font.copy()
        self.font.configure(size=20)

        self.widget_config()

    def widget_config(self):
        self.title_label.configure(
            text=self.title,
            font=self.font
        )