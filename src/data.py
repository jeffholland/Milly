import json

entries = []

last_filepath = ""

def load(filepath):
    try:
        f = open(filepath, "r")
    except OSError:
        print("Load Error: filepath could not be read")

    with f:
        global entries
        entries = json.load(f)

    global last_filepath
    last_filepath = filepath

def save(filepath):
    with open(filepath, "w") as f:
        json.dump(entries, f)

    global last_filepath
    last_filepath = filepath

def clear():
    entries.clear()

def get_entries():
    return entries

def get_last_filepath(short=False):
    if short:
        # strip "json/" and ".json"
        return last_filepath[5:-5]
    return last_filepath

def change_detected():
    # No entries means no changes
    if len(entries) == 0:
        return True

    # Entries and no last filepath 
    # means something changed
    if len(last_filepath) == 0:
        return False

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

def add_entry(text):
    entries.append(
        {
            "date": str(date.today()),
            "time": datetime.now().strftime("%I:%M %p"),
            "text": text
        }
    )

def remove_entry(index):
    entries.pop(index)

def swap_entry(index1, index2):
    tmp = entries[index1]
    entries[index1] = entries[index2]
    entries[index2] = tmp