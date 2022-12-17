# debug mode on/off

DEBUG = True

# dimensions

WIDTH = 800
HEIGHT = 960

MODE = "normal"
# MODE = "fullscreen"

INPUT_HEIGHT = 7

if MODE == "fullscreen":
    INPUT_WIDTH = 110
else:
    INPUT_WIDTH = 50

ENTRY_HEIGHT = 80


# format settings

PADDING = 10



# fonts

ENTRY_FONT_SIZE = 14
ENTRY_FONT_FAMILY = "Helvetica"

INPUT_FONT_SIZE = 18
INPUT_FONT_FAMILY = "American Typewriter"