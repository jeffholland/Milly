import json

entries = []

def load(filepath):
    with open(filepath, 'r') as f:
        global entries
        entries = json.load(f)

def save(filepath):
    with open(filepath, "w") as f:
        f.write(json.dumps(entries))

def get_entries():
    return entries



from datetime import date

def add_entry(text):
    entries.append(
        {
            "date": str(date.today()),
            "text": text
        }
    )