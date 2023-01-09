from tkinter import messagebox

import json

from constants import SAVE_DATA_PATH
from datetime import date, datetime

data = {}
entries = []

last_filepath = ""

def get_last_filepath(short=False):
    if short:
        # strip the folder path and the .json extension
        index = len(SAVE_DATA_PATH)
        shortened = last_filepath[index:-5]
        return shortened
    return last_filepath

def change_detected():
    # No entries means no changes
    if len(entries) == 0:
        return False

    # Entries and no last filepath 
    # means something changed
    if len(last_filepath) == 0:
        return True

    try:
        f = open(last_filepath)
    except OSError:
        messagebox.showerror("Change detection error", "Change detection error: Filepath could not be read")
        return False

    with f:
        loaded = json.load(f)
        if data == loaded:
            return False

        # Uncomment to debug - see what's different

        for entry in loaded["entries"]:
            print(entry)
        print("\n")
        for entry in data["entries"]:
            print(entry)
        print("\n")
        for group in loaded["groups"]:
            print(group)
        print("\n")
        for entry in data["groups"]:
            print(entry)

    
    return True




# Load / Save / Clears

def load_entries(filepath):
    try:
        f = open(filepath, "r")
    except OSError:
        messagebox.showerror("Load error", "Load error: filepath could not be read")
        return

    with f:
        global data
        global entries
        try:
            data = json.load(f)
            entries = data["entries"]
        except json.decoder.JSONDecodeError:
            # File is empty, ignore.
            # (to the user, it will look like an empty file was just loaded,
            # which is fine because that's apparently what they wanted!)
            return

    global last_filepath
    last_filepath = filepath

def save_entries(filepath):
    with open(filepath, "w") as f:
        json.dump(data, f)

    global last_filepath
    last_filepath = filepath

def save_groups(groups):
    data["groups"] = groups

def clear_entries():
    entries.clear()



# Getter functions

def get_data():
    return data

def get_entries():
    return entries

def get_num_entries():
    return len(entries)

def get_num_unchecked_entries():
    num_unchecked_entries = 0

    for entry in entries:
        try:
            if entry["checked"] == False:
                num_unchecked_entries += 1
        except KeyError:
            num_unchecked_entries += 1

    return num_unchecked_entries



# Entry generation function

def create_entry(text, index=None, group=None):
    if not index:
        index = len(entries)

    if group:
        return {
            "date": date.strftime(date.today(), "%A") + " " + str(date.today()),
            "time": datetime.now().strftime("%I:%M %p"),
            "text": text,
            "group": group,
            "index": index
        }
    return {
        "date": date.strftime(date.today(), "%A") + " " + str(date.today()),
        "time": datetime.now().strftime("%I:%M %p"),
        "text": text,
        "group": "None",
        "index": index
    }

def add_entry(text, group=None):
    entries.append(create_entry(text, group=group))

def remove_entry(index):
    for i in range(len(entries)):
        if int(entries[i]["index"]) == index:
            entries.pop(i)
            break

def swap_entry(index1, index2):
    tmp = entries[index1]
    entries[index1] = entries[index2]
    entries[index2] = tmp

def insert_entry(index, text):
    entries.insert(index, create_entry(text, index=index))

def move_entry(index1, index2):
    tmp = entries.pop(index1)
    entries.insert(index2, tmp)