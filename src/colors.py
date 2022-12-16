import json
from os import scandir

# pick your starting color scheme here
# they are sorted alphabetically

COLOR_SCHEME_IDX = 6

COLOR_SCHEMES = []

global colors
colors = []


def load_colors():
    if (len(COLOR_SCHEMES) == 0):
        with scandir("json/color_schemes/") as entries:
            for entry in entries:
                COLOR_SCHEMES.append(entry.name[:-5])
    
    COLOR_SCHEMES.sort()

    scheme_name = COLOR_SCHEMES[COLOR_SCHEME_IDX]

    filepath = f"json/color_schemes/{scheme_name}.json"

    with open(filepath, 'r') as f:
        global colors
        colors = json.load(f)


def get_colors():
    global colors
    return colors


def get_color_schemes():
    return COLOR_SCHEMES


def get_current_color_scheme():
    return COLOR_SCHEMES[COLOR_SCHEME_IDX]


def switch_color_scheme(dir="right"):
    global colors
    global COLOR_SCHEME_IDX

    if (dir == "left"):
        if COLOR_SCHEME_IDX <= 0:
            COLOR_SCHEME_IDX = len(COLOR_SCHEMES) - 1
        else:
            COLOR_SCHEME_IDX -= 1
    else:
        if COLOR_SCHEME_IDX >= len(COLOR_SCHEMES) - 1:
            COLOR_SCHEME_IDX = 0
        else:
            COLOR_SCHEME_IDX += 1
    
    load_colors()

def set_color_scheme(name):
    global COLOR_SCHEME_IDX
    global COLOR_SCHEMES

    index = COLOR_SCHEMES.index(name)
    
    if index >= 0 and index < len(COLOR_SCHEMES):
        COLOR_SCHEME_IDX = index

        load_colors()

def new_color_scheme(scheme):
    filepath = f"json/color_schemes/new_scheme.json"

    with open(filepath, "w") as f:
        json.dump(scheme, f)