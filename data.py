entries = []

from datetime import date

def add_entry(text):
    entries.append(
        {
            "date": date.today(),
            "text": text
        }
    )