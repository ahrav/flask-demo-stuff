"""
libs.strings

By default user en-us.json file inside strings
"""
import json

default_local = "en-us"
cached_strings = {}


def refresh():
    global cached_strings
    with open(f"strings/{default_local}.json") as f:
        cached_strings = json.load(f)


def gettext(name):
    return cached_strings[name]


refresh()
