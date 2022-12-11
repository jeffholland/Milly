from colors import switch_color_scheme

class Key:
    def __init__(self, master):
        self.master = master
        self.keys_pressed = {
            "cmd": False,
            "shift": False
        }
        self.just_submitted = False

    def key_press(self, event):

        # Holding down CMD or Shift
        if "Meta" in event.keysym:
            self.keys_pressed["cmd"] = True
        if "Shift" in event.keysym:
            self.keys_pressed["shift"] = True

        # Return to submit, shift+return for newline
        if event.keysym == "Return" and self.keys_pressed["shift"] == False:
            self.master.submit()
            self.just_submitted = True
        
        # Cmd+i to insert
        # Cmd+s to save
        # Cmd+l to load
        # Cmd+c to clear
        # Cmd+backspace to remove first entry
        # Cmd+shift+backspace to remove last entry

        if self.keys_pressed["cmd"] == True:
            if event.keysym == "i":
                self.master.insert()
            if event.keysym == "s":
                self.master.save()
            if event.keysym == "l":
                self.master.load()
            if event.keysym == "c":
                self.master.clear()
            if event.keysym == "BackSpace":
                if self.keys_pressed["shift"] == True:
                    self.master.remove_last_entry()
                else:
                    self.master.remove_first_entry()
            if event.keysym == "Left":
                switch_color_scheme("left")
                self.master.master.refresh_colors()
            if event.keysym == "Right":
                switch_color_scheme("right")
                self.master.master.refresh_colors()


    def key_release(self, event):
        if "Meta" in event.keysym:
            self.keys_pressed["cmd"] = False
        if "Shift" in event.keysym:
            self.keys_pressed["shift"] = False

        if self.just_submitted == True:
            if event.keysym == "Return":
                self.master.input.delete("1.0", "end")
            self.just_submitted = False