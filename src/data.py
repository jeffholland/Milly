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
        "text": text,
        "id": hashlib.sha256(str.encode(text)).hexdigest()
    }

def add_entry(text, group_index=None):
    entry = create_entry(text)
    print(group_index)
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
    if group:
        data["groups"][group].pop(index)
    
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



# Group functions

def move_entry_to_group(entry_index, entry_group, group_index):
    entry = None

    for group in data["groups"]:
        if group["name"] == entry_group:
            entry = group["entries"].pop(entry_index)

    if entry:
        data["groups"][group_index]["entries"].append(entry)

def rename_group(group, new_name):
    tmp = data["groups"].pop(group)
    data["groups"][new_name] = tmp

def move_group(name, dir):

    count = 0
    
    global data

    try:
        group_list = data["group_list"]
    except KeyError:
        data["group_list"] = []

    if len(data["group_list"]) == 0:
        for group in data["groups"]:
            data["group_list"].append(group)
    
    tmp = data["group_list"]
        
    print(f"data.py - move_group - middle of function: {tmp}")

    for group_name in data["group_list"]:
        if group_name == name:
            if dir == "up":
                if count > 0:
                    swap_groups(count, count - 1)
            if dir == "down":
                if count < len(group_list) - 1:
                    swap_groups(count, count + 1)
            break

        count += 1

    tmp = data["group_list"]
    print(f"data.py - move_group - end of function: {tmp}")

def swap_groups(pos1, pos2):
    global data
    data["group_list"][pos1], data["group_list"][pos2] = data["group_list"][pos2], data["group_list"][pos1]

# def set_group_list(group_list):
#     data["group_list"] = group_list



# Getter functions

def get_data():
    try:
        tmp = data["group_list"]
        print(f"data.py - get_data: {tmp}")
    except KeyError:
        pass
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