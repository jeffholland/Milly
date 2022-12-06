import json

with open('data.json', 'r') as f:
    entries = json.load(f)

from datetime import date

def add_entry(text):
    entries.append(
        {
            "date": str(date.today()),
            "text": text
        }
    )

def save():
    with open("data.json", "w") as f:
        f.write(json.dumps(entries))