from tkinter import messagebox

import json
import hashlib

from constants import SAVE_DATA_PATH
from datetime import date, datetime

data = {}

last_filepath = ""

#
# KEEP EDITING THIS UNTIL IT ALL WORKS WITH "test.json"
# then do entries.py and input.py and anything else that needs editing
#


# Was change detected since the last time the data was saved?
# Returns a bool answering that question

def change_detected():
    try:
        # No groups and no entries means no changes
        if len(data["groups"]) == 0 and len(data["entries"]) == 0:
            return False
    except KeyError:
        # JSON format requirement: 
        # there must be "groups" and "entries" keys.
        messagebox.showerror("Incompatible data", 
            """
            Error: this save data is in an incompatible format. 
            Please load a different file.
            """
        )

    # If there is data, and there's no last saved filepath,
    # something definitely changed.
    if len(last_filepath) == 0:
        return True


    # Get current data to check against
    try:
        f = open(last_filepath)
    except OSError:
        messagebox.showerror("Change detection error", "Change detection error: Filepath could not be read")
        return False

    # Load JSON and check current data against 
    # loaded data to find changes
    with f:
        loaded = json.load(f)
        if data == loaded:
            return False
    
    return True



# Get the filepath of the last file saved/loaded.
# the boolean arg determines whether you get the full file path,
# or just the name.

def get_last_filepath(short=False):
    if short:
        # strip the folder path and the .json extension
        index = len(SAVE_DATA_PATH)
        shortened = last_filepath[index:-5]
        return shortened
    return last_filepath



# Load data

def load_entries(filepath):
    # Try to open the file
    try:
        f = open(filepath, "r")
    except OSError:
        messagebox.showerror("Load error", 
            f"Error: filepath {filepath} could not be loaded")
        return

    with f:
        global data
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            # File is empty, ignore.
            # (to the user, it will look like an empty file was just loaded,
            # which is fine because that's apparently what they wanted!)
            return

    global last_filepath
    last_filepath = filepath

def save_all(filepath):
    # Dump the data dict into the filepath passed as an argument
    with open(filepath, "w") as f:
        json.dump(data, f)

    global last_filepath
    last_filepath = filepath

def clear_entries():
    data.clear()



# Getter functions

def get_data():
    return data

def get_num_entries():
    count = 0
    # fix this!!!
    try:
        for group in data["groups"]:
            count += len(data["groups"][group])
    except KeyError:
        data["groups"] = []

    try:
        count += len(data["entries"])
    except KeyError:
        data["entries"] = []



# Entry generation function

def create_entry(text, index=None):
    if not index:
        try:
            index = len(data["entries"])
        except KeyError:
            data["entries"] = []
            index = len(data["entries"])

    return {
        "date": date.strftime(date.today(), "%A") + " " + str(date.today()),
        "time": datetime.now().strftime("%I:%M %p"),
        "text": text,
        "id": hashlib.sha256(str.encode(text)).hexdigest()
    }

def add_entry(text, group=None):
    entry = create_entry(text)
    print(entry)
    if group:
        try:
            data["groups"][group].append(entry)
        except KeyError:
            data["groups"][group] = []
            data["groups"][group].append(entry)
    try:
        data["entries"].append(entry)
    except KeyError:
        data["entries"] = []
        data["entries"].append(entry)

def add_group(name):
    data["groups"][name] = []

def remove_entry(index):
    comp = 0
    for group in list(data["groups"].keys()):
        num_in_group = len(data["groups"][group])
        comp += num_in_group
        if comp > index:
            data["groups"][group].pop(index - (comp - num_in_group))
            return
    
    for count in range(len(data["entries"])):
        if count == index:
            data["entries"].pop(index)

def swap_entry(index1, index2):
    if index1 == index2:
        return
    tmp = data["entries"][index1]
    data["entries"][index1] = data["entries"][index2]
    data["entries"][index2] = tmp

def insert_entry(index, text):
    data["entries"].insert(index, create_entry(text, index=index))

def move_entry(group, text, dir):
    data_array = []

    if group == None:
        data_array = data["entries"]

    else:
        data_array = data["groups"][group]

    count = 0
    num_entries = len(data_array)

    for entry in data_array:

        if entry["text"] == text:

            data_array.pop(count)

            if dir == "top":
                index = 0
            elif dir == "bottom":
                index = num_entries - 1
            elif dir == "up":
                if count > 0:
                    index = count - 1
                else:
                    index = count
            elif dir == "down":
                if count < num_entries - 1:
                    index = count + 1
                else:
                    index = count
            data_array.insert(index, entry)
            return
        
        count += 1


def move_entry_to_group(entry_index, entry_group, group):
    if entry_group:
        entry = data["groups"][entry_group].pop(entry_index)
    else:
        entry = data["entries"].pop(entry_index)
    
    data["groups"][group].append(entry)