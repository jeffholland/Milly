from tkinter import messagebox

import json
import hashlib

from constants import SAVE_DATA_PATH
from datetime import date, datetime


# All save data is stored here

data = {}


# Last loaded/saved filepath as a string

last_filepath = ""



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


# Save data

def save_all(filepath):
    # Dump the data dict into the filepath passed as an argument
    with open(filepath, "w") as f:
        json.dump(data, f)

    global last_filepath
    last_filepath = filepath


# Clear data

def clear_entries():
    data.clear()



# Was change detected since the last time the data was saved?
# Returns a bool answering that question

def change_detected():
    try:
        # No groups and no entries means no changes
        if len(data["groups"]) == 0 and len(data["entries"]) == 0:
            return False
    except KeyError:
        # If the data hasn't even been properly initialized yet,
        # then we can't say change has been detected.
        return False

    # If there is data, and there's no last saved filepath,
    # something must have changed.
    if len(last_filepath) == 0:
        return True


    # Get current data to check against
    try:
        f = open(last_filepath)
    except OSError:
        messagebox.showerror("Change detection error", 
            "Change detection error: Filepath could not be read")
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



# Entry generation function

def create_entry(text):
    return {
        "date": date.strftime(date.today(), "%A") + " " + str(date.today()),
        "time": datetime.now().strftime("%I:%M %p"),
        "text": text
    }

def add_entry(text, group_index=None):
    entry = create_entry(text)
    if group_index != None:
        try:
            data["groups"][group_index]["entries"].append(entry)
        except KeyError:
            data["groups"][group_index]["entries"] = []
            data["groups"][group_index]["entries"].append(entry)
        return
    try:
        data["entries"].append(entry)
    except KeyError:
        data["entries"] = []
        data["entries"].append(entry)

def add_group(name):
    data["groups"].append(
        {
            "name": name,
            "entries": []
        }
    )

def remove_entry(index, group=None):
    if group != None:
        group_index = get_group_index(group)
        data["groups"][group_index]["entries"].pop(index)
    else:
        for count in range(len(data["entries"])):
            if count == index:
                data["entries"].pop(index)

def remove_group(group):
    index = get_group_index(group)
    group = data["groups"].pop(index)

    for entry in group["entries"]:
        data["entries"].append(entry)

def swap_entry(index1, index2):
    if index1 == index2:
        return
    tmp = data["entries"][index1]
    data["entries"][index1] = data["entries"][index2]
    data["entries"][index2] = tmp

def insert_entry(index, text):
    if index < len(data["entries"]) - 1:
        data["entries"].insert(index, create_entry(text))
    else:
        add_entry(text)

def move_entry(group, index, dir):
    global data
    new_index = index
    data_array = []

    if group != None:
        group_index = get_group_index(group)
        data_array = data["groups"][group_index]["entries"]
    else:
        data_array = data["entries"]

    if dir == "top":
        new_index = 0
    if dir == "bottom":
        new_index = len(data["groups"][group_index]["entries"])
    if dir == "up":
        new_index = index - 1
    if dir == "down":
        new_index = index + 1

    if new_index != index:
        entry = data_array.pop(index)
        data_array.insert(new_index, entry)



# Group functions

def move_entry_to_group(entry_index, entry_group, group_index):
    entry = None

    if entry_group == None:
        entry = data["entries"].pop(entry_index)
    else:
        for group in data["groups"]:
            if group["name"] == entry_group:
                entry = group["entries"].pop(entry_index)

    if entry:
        data["groups"][group_index]["entries"].append(entry)

def rename_group(group, new_name):
    index = get_group_index(group)
    data["groups"][index]["name"] = new_name

def move_group(name, dir):
    global data

    index = get_group_index(name)

    if index != None:
        if dir == "up":
            if index > 0:
                group = data["groups"].pop(index)
                data["groups"].insert(index - 1, group)
        if dir == "down":
            if index < len(data["groups"]) - 1:
                group = data["groups"].pop(index)
                data["groups"].insert(index + 1, group)

def get_group_index(name):
    count = 0
    for group in data["groups"]:
        if group["name"] == name:
            return count
        count += 1
    return None



# Getter functions

def get_data():
    return data

def get_num_entries():
    count = 0
    try:
        for group in data["groups"]:
            count += len(group["entries"])
    except KeyError:
        data["groups"] = {}

    try:
        count += len(data["entries"])
    except KeyError:
        data["entries"] = []
    
    return count