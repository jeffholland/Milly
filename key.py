class Key:
    def __init__(self, master):
        self.master = master
        self.keys_pressed = {
            "Meta_L": False
        }
        self.just_submitted = False

    def key_press(self, event):

        if event.keysym == "Meta_L":
            self.keys_pressed["Meta_L"] = True
        
        if self.keys_pressed["Meta_L"] == True:
            if event.keysym == "Return":
                self.master.submit()
                self.just_submitted = True
            if event.keysym == "s":
                self.master.save()
            if event.keysym == "l":
                self.master.load()
            if event.keysym == "c":
                self.master.clear()

    def key_release(self, event):
        for key in self.keys_pressed.keys():
            if key == event.keysym:
                self.keys_pressed[key] = False

        if self.just_submitted == True:
            if event.keysym == "Return":
                self.master.input.delete("1.0", "end")
            self.just_submitted = False