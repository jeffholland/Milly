class Key:
    def __init__(self, master):
        self.master = master
        self.keys_pressed = {
            "cmd": False
        }
        self.just_submitted = False

    def key_press(self, event):

        if event.keysym == "Meta_L" or event.keysym == "Meta_R":
            self.keys_pressed["cmd"] = True
        
        if self.keys_pressed["cmd"] == True:
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
        if event.keysym == "Meta_L" or event.keysym == "Meta_R":
            self.keys_pressed["cmd"] = False

        if self.just_submitted == True:
            if event.keysym == "Return":
                self.master.input.delete("1.0", "end")
            self.just_submitted = False