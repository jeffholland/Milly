from colors import switch_color_scheme
from data import get_num_entries

class Key:
    def __init__(self, master):
        self.master = master
        self.keys_pressed = {
            "cmd": False,
            "shift": False
        }
        self.just_submitted = False
        self.edit_selection_mode = False
        self.edit_selection_index = 0

    def key_press(self, event):

        # Holding down CMD or Shift
        if "Meta" in event.keysym:
            self.keys_pressed["cmd"] = True
        if "Shift" in event.keysym:
            self.keys_pressed["shift"] = True

        # see shortcuts.txt for a list of all shortcuts

        if event.keysym == "Return" and self.keys_pressed["shift"] == False:
            self.master.submit()
            self.just_submitted = True
        
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
            if event.keysym == "e":
                if get_num_entries() > 0:
                    # Enter or exit edit selection mode
                    self.edit_selection_mode = not self.edit_selection_mode
                    self.master.master.top_frame.entries[self.edit_selection_index].edit_selected(self.edit_selection_mode)
            
        # Edit selection mode
        
        if self.edit_selection_mode:

            if event.keysym == "Down":
                # Change edit selected entry down
                self.master.master.top_frame.entries[self.edit_selection_index].edit_selected(False)
                self.edit_selection_index += 1
                if self.edit_selection_index >= get_num_entries():
                    self.edit_selection_index = 0
                self.master.master.top_frame.entries[self.edit_selection_index].edit_selected(True)

            if event.keysym == "Up":
                # Change edit selected entry up
                self.master.master.top_frame.entries[self.edit_selection_index].edit_selected(False)
                self.edit_selection_index -= 1
                if self.edit_selection_index < 0:
                    self.edit_selection_index = get_num_entries() - 1
                self.master.master.top_frame.entries[self.edit_selection_index].edit_selected(True)

            if event.keysym == "Return":
                # Execute selected entry's edit mode
                self.master.master.top_frame.entries[self.edit_selection_index].edit_pressed()




    def key_release(self, event):
        if "Meta" in event.keysym:
            self.keys_pressed["cmd"] = False
        if "Shift" in event.keysym:
            self.keys_pressed["shift"] = False

        if self.just_submitted == True:
            if event.keysym == "Return":
                self.master.input.delete("1.0", "end")
            self.just_submitted = False