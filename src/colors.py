import json

COLOR_SCHEME_IDX = 0

COLOR_SCHEMES = [
    "b&w",
    "orange",
    "teal",
    "purplegreen",
    "redblue",
    "pink"
]

global colors
with open("json/color_schemes/b&w.json", "r") as f:
    colors = json.load(f)

def load_colors():
    scheme_name = COLOR_SCHEMES[COLOR_SCHEME_IDX]

    filepath = f"json/color_schemes/{scheme_name}.json"

    with open(filepath, 'r') as f:
        global colors
        colors = json.load(f)

def get_colors():
    global colors
    return colors


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