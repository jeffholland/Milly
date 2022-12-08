import json

entries = []

last_filepath = ""

def load(filepath):
    with open(filepath, 'r') as f:
        global entries
        entries = json.load(f)

    global last_filepath
    last_filepath = filepath

def save(filepath):
    with open(filepath, "w") as f:
        json.dump(entries, f)

def clear():
    entries.clear()

def get_entries():
    return entries

def get_last_filepath():
    return last_filepath



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