import platform


# general

PLATFORM = platform.system()

MODE = "normal"
# MODE = "fullscreen"

CONFIG = "interpret"
# CONFIG = "build"



# File paths

if CONFIG == "interpret":
    JSON_PATH = "json/"
    EXPORT_PATH = "export/"
if CONFIG == "build":
    JSON_PATH = "../../json/"
    EXPORT_PATH = "../../export/"

COLOR_SCHEME_PATH = JSON_PATH + "color_schemes/"
SETTINGS_PATH = JSON_PATH + "settings.json"


# dimensions

WIDTH = 800
HEIGHT = 960

ENTRY_HEIGHT = 80




# format settings

PADDING = 10
PADDING_BIG = 40


# fonts

ENTRY_FONT_SIZE = 14
ENTRY_FONT_FAMILY = "Helvetica"

INPUT_FONT_SIZE = 17
INPUT_FONT_FAMILY = "Helvetica"