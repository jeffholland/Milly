from tkinter import messagebox

from data import get_num_entries
from constants import *

class Key:
    def __init__(self, master):
        self.master = master

        # Booleans
        self.keys_pressed = {
            "cmd": False,
            "shift": False,
            "alt": False
        }
        self.just_submitted = False
        self.edit_selection_mode = False

        # Edit selection
        self.edit_selection_index = 0

        if PLATFORM == "Windows":
            self.cmd_key = "Control"
        else:
            self.cmd_key = "Meta"

    def key_press(self, event):

        # Holding down CMD or Shift
        if self.cmd_key in event.keysym:
            self.keys_pressed["cmd"] = True
        if "Shift" in event.keysym:
            self.keys_pressed["shift"] = True
        if "Alt" in event.keysym:
            self.keys_pressed["alt"] = True

        # see shortcuts.txt for a list of all shortcuts

        if (event.keysym == "Return" 
            and self.keys_pressed["shift"] == False):
            
            # cmd+return to submit to top group
            group_index = None
            if self.keys_pressed["cmd"]:
                if len(self.master.master.top_frame.get_group_names()) > 0:
                    group_index = 0
            
            self.master.submit(group_index=group_index)
            self.just_submitted = True
        
        # cmd key pressed

        if self.keys_pressed["cmd"] == True:

            if event.keysym.lower() == "i":
                self.master.insert()

            if event.keysym.lower() == "s" and self.keys_pressed["shift"] == False:
                self.master.save()

            if event.keysym.lower() == "l":
                self.master.load()

            if event.keysym.lower() == "c":
                self.master.clear()

            if event.keysym.lower() == "b":
                self.master.load()
                self.master.input_path.browser.show_browser()

            if event.keysym.lower() == "g":
                self.master.show_groups()

            if event.keysym == "BackSpace":
                if self.keys_pressed["shift"] == True:
                    self.master.remove_last_entry()
                else:
                    self.master.remove_first_entry()

            if event.keysym == "Left":
                self.master.master.settings.color_scheme_settings.dcs_switch("left")
                # self.master.master.colors_obj.switch_color_scheme("left")
                self.master.master.refresh_colors()

            if event.keysym == "Right":
                self.master.master.settings.color_scheme_settings.dcs_switch("right")
                # self.master.master.colors_obj.switch_color_scheme("right")
                self.master.master.refresh_colors()

            if event.keysym.lower() == "e":
                if get_num_entries() > 0:
                    # Enter or exit edit selection mode
                    self.edit_selection_mode = not self.edit_selection_mode
                    self.master.master.top_frame.entries[self.edit_selection_index].edit_selected(self.edit_selection_mode)

            if event.keysym.lower() == "f" and not self.keys_pressed["shift"]:
                self.master.show_find_window()

            if event.keysym == "comma":
                self.master.master.show_settings()

            if PLATFORM == "Windows":
                if event.keysym.lower() == "w":
                    self.master.destroy()

            # cmd+shift
            if self.keys_pressed["shift"] == True:

                # cmd+shift+f to remove any filter
                if event.keysym.lower() == "f":
                    self.master.master.top_frame.remove_filter()

                # cmd+shift+h to show/hide checkboxes
                if event.keysym.lower() == "h":
                    self.master.master.show_hide_checks()

                # cmd+shift+x to bring up the export window
                if event.keysym.lower() == "x":
                    self.master.export()

                # cmd+shift+s to bring up the stats window
                if event.keysym.lower() == "s":
                    self.master.show_stats()

        # endif cmd key pressed
            
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
                self.edit_selection_mode = False




    def key_release(self, event):
        if self.cmd_key in event.keysym:
            self.keys_pressed["cmd"] = False
        if "Shift" in event.keysym:
            self.keys_pressed["shift"] = False
        if "Alt" in event.keysym:
            self.keys_pressed["alt"] = False

        if event.keysym == "Return":
            if self.just_submitted:
                self.master.input.delete("1.0", "end")
                self.just_submitted = False