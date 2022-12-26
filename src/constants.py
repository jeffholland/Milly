import platform
from os import path


# general

PLATFORM = platform.system()

MODE = "normal"
# MODE = "fullscreen"

# CONFIG = "build"
CONFIG = "run"



# file paths

HOME_DIR = path.expanduser("~")

ABS_PATH = HOME_DIR + "/Dev/Python/tkinter/milly/"

if CONFIG == "build":
    ABS_PATH = ABS_PATH + "dist/milly/"

JSON_PATH = ABS_PATH + "json/"
EXPORT_PATH = ABS_PATH + "export/"

COLOR_SCHEME_PATH = JSON_PATH + "color_schemes/"
SAVE_DATA_PATH = JSON_PATH + "save_data/"
SETTINGS_PATH = JSON_PATH + "settings.json"



# dimensions

WIDTH = 800
HEIGHT = 960

ENTRY_HEIGHT = 80

PADDING = 10
PADDING_BIG = 40



# fonts

ENTRY_FONT_SIZE = 14
ENTRY_FONT_FAMILY = "Helvetica"

INPUT_FONT_SIZE = 17
INPUT_FONT_FAMILY = "Helvetica"