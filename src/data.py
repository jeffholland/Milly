import json

entries = []

last_filepath = ""

def get_last_filepath(short=False):
    if short:
        # strip "json/" and ".json"
        return last_filepath[5:-5]
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
        print("Change detection error: Filepath could not be read")
        return False

    with f:
        if entries == json.load(f):
            return False
    
    return True


# Entry functions

from datetime import date, datetime

def load_entries(filepath):
    try:
        f = open(filepath, "r")
    except OSError:
        print("Load Error: filepath could not be read")

    with f:
        global entries
        entries = json.load(f)

    global last_filepath
    last_filepath = filepath

def save_entries(filepath):
    with open(filepath, "w") as f:
        json.dump(entries, f)

    global last_filepath
    last_filepath = filepath

def clear_entries():
    entries.clear()

def get_entries():
    return entries

def get_num_entries():
    return len(entries)

def create_entry(text):
    return {
        "date": date.strftime(date.today(), "%A") + " " + str(date.today()),
        "time": datetime.now().strftime("%I:%M %p"),
        "text": text
    }

def add_entry(text):
    entries.append(create_entry(text))

def remove_entry(index):
    entries.pop(index)

def swap_entry(index1, index2):
    tmp = entries[index1]
    entries[index1] = entries[index2]
    entries[index2] = tmp

def insert_entry(index, text):
    entries.insert(index, create_entry(text))