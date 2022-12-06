import json

entries = []

def load(filepath):
    with open(filepath, 'r') as f:
        global entries
        entries = json.load(f)

def save(filepath):
    with open(filepath, "w") as f:
        json.dump(entries, f)

def clear():
    entries.clear()

def get_entries():
    return entries



from datetime import date, datetime

def add_entry(text):
    entries.append(
        {
            "date": str(date.today()),
            "time": datetime.now().strftime("%I:%M %p"),
            "text": text
        }
    )