import re


def replace_special(string):
    return re.sub('[^a-zA-Z0-9_]', '', string)
