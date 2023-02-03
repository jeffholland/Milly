import os
import json

from constants import *

def install():
    dirs = [
        ABS_PATH,
        DATA_PATH,
        JSON_PATH,
        COLOR_SCHEME_PATH,
        SAVE_DATA_PATH,
        EXPORT_PATH
    ]

    for dir in dirs:
        if not os.path.exists(dir):
            os.mkdir(dir)

    set_default_color_scheme()

    create_settings()



def set_default_color_scheme():
    schemes = os.listdir(COLOR_SCHEME_PATH)
    if len(schemes) == 0:
        filepath = COLOR_SCHEME_PATH + "default.json"
        scheme = {
            "BG1": "#1D1E2C",
            "BG2": "#AC9FBB",
            "HL1": "#AC9FBB",
            "HL2": "#F7EBEC"
        }
        with open(filepath, "w") as f:
            json.dump(scheme, f)


def create_settings():
    if not os.path.exists(SETTINGS_PATH):
        settings = {
            "default_color_scheme": "default",
            "show_checkboxes": 1,
            "show_menu": 1,
            "show_times": 1,
            "show_dates": 1,
            "font_family": "Helvetica"
        }
        with open(SETTINGS_PATH, "w") as f:
            json.dump(settings, f)