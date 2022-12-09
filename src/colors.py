COLOR_SCHEME_IDX = 0

COLOR_SCHEMES = [
    # b&w
    {
        "BG1": "black",
        "BG2": "gray",
        "HL1": "lightgray",
        "HL2": "white"
    },
    # orange
    {
        "BG1": "#7A432B",
        "BG2": "#7A2906",
        "HL1": "#FB8958",
        "HL2": "#FA540C"
    },
    # teal
    {
        "BG1": "#005F61",
        "BG2": "#1D6061",
        "HL1": "#00DDE0",
        "HL2": "#35E3E6"
    },
    # purplegreen
    {
        "BG1": "#760A8F",
        "BG2": "#BE3BDB",
        "HL1": "#98DB3C",
        "HL2": "#BCFF5E"
    },
    # redblue
    {
        "BG1": "#E00D14",
        "BG2": "#041E94",
        "HL1": "#022BE0",
        "HL2": "#E0BA19"
    }
]

colors = COLOR_SCHEMES[COLOR_SCHEME_IDX]

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
    
    colors = COLOR_SCHEMES[COLOR_SCHEME_IDX]
    print(colors["BG2"])